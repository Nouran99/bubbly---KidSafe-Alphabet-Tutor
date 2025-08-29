"""
ASR (Automatic Speech Recognition) Module
Uses faster-whisper for efficient speech-to-text with VAD
Author: Nouran Darwish
"""

import numpy as np
from faster_whisper import WhisperModel
import torch
import logging
from typing import Tuple, Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ASRProcessor:
    """
    ASR processor using faster-whisper with VAD
    Optimized for low latency (<500ms)
    """
    
    def __init__(self, model_size: str = "small.en", device: str = "cpu"):
        """
        Initialize ASR with faster-whisper
        Args:
            model_size: Model size (tiny.en, base.en, small.en)
            device: Device to use (cpu or cuda)
        """
        logger.info(f"Initializing ASR with model: {model_size}")
        
        # Initialize Whisper model with optimizations
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type="int8" if device == "cpu" else "float16",
            num_workers=2,
            download_root="models/"
        )
        
        # Initialize Silero VAD for voice activity detection
        self.vad_model, self.vad_utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=False,
            trust_repo=True
        )
        
        self.sample_rate = 16000
        logger.info("ASR initialized successfully")
        
    def transcribe(self, audio_input: np.ndarray, language: str = "en") -> Tuple[str, float]:
        """
        Transcribe audio to text with confidence score
        Target latency: 300-500ms
        
        Args:
            audio_input: Audio data as numpy array
            language: Language code (default: en)
            
        Returns:
            Tuple of (transcription, confidence_score)
        """
        try:
            start_time = time.time()
            
            # Preprocess audio
            audio = self._preprocess_audio(audio_input)
            
            # Check for voice activity
            if not self._has_voice_activity(audio):
                logger.info("No voice activity detected")
                return "", 0.0
            
            # Transcribe with faster-whisper
            segments, info = self.model.transcribe(
                audio,
                language=language,
                beam_size=1,  # Faster with beam_size=1
                best_of=1,
                temperature=0.0,  # Deterministic
                vad_filter=True,
                vad_parameters={
                    "threshold": 0.5,
                    "min_speech_duration_ms": 250,
                    "max_speech_duration_s": 5,
                    "min_silence_duration_ms": 150
                }
            )
            
            # Extract transcription and confidence
            transcription = ""
            confidence_scores = []
            
            for segment in segments:
                transcription += segment.text.strip() + " "
                if hasattr(segment, 'avg_logprob'):
                    # Convert log probability to confidence score
                    confidence = np.exp(segment.avg_logprob)
                    confidence_scores.append(confidence)
            
            transcription = transcription.strip()
            avg_confidence = np.mean(confidence_scores) if confidence_scores else 0.5
            
            elapsed = time.time() - start_time
            logger.info(f"Transcription completed in {elapsed:.3f}s: '{transcription}' (conf: {avg_confidence:.2f})")
            
            return transcription, float(avg_confidence)
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return "", 0.0
    
    def _preprocess_audio(self, audio_input: np.ndarray) -> np.ndarray:
        """
        Preprocess audio for transcription
        """
        # Handle different input formats
        if isinstance(audio_input, tuple):
            sample_rate, audio = audio_input
            # Resample to 16kHz if needed
            if sample_rate != self.sample_rate:
                import librosa
                audio = librosa.resample(
                    audio.astype(np.float32),
                    orig_sr=sample_rate,
                    target_sr=self.sample_rate
                )
        else:
            audio = audio_input
            
        # Convert to float32 if needed
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
            
        # Normalize audio
        if audio.max() > 1.0:
            audio = audio / 32768.0
            
        # Convert stereo to mono if needed
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
            
        return audio
    
    def _has_voice_activity(self, audio: np.ndarray, threshold: float = 0.5) -> bool:
        """
        Check if audio contains voice activity using Silero VAD
        """
        try:
            # Prepare audio for VAD
            if len(audio) < 512:
                return False
                
            # Convert to tensor
            audio_tensor = torch.from_numpy(audio).float()
            
            # Get VAD confidence
            confidence = self.vad_model(audio_tensor, self.sample_rate).item()
            
            return confidence > threshold
            
        except Exception as e:
            logger.warning(f"VAD check failed: {e}")
            # Fallback to energy-based detection
            return np.max(np.abs(audio)) > 0.01
    
    def process_streaming(self, audio_chunk: np.ndarray) -> Optional[str]:
        """
        Process audio chunk for streaming transcription
        """
        # For streaming, accumulate chunks and process when VAD detects end of speech
        # This is a simplified version - full implementation would maintain state
        if self._has_voice_activity(audio_chunk):
            # Continue accumulating
            return None
        else:
            # End of speech detected, process accumulated audio
            transcription, _ = self.transcribe(audio_chunk)
            return transcription if transcription else None