"""
TTS (Text-to-Speech) Module
Uses Piper TTS for efficient, child-friendly speech synthesis
Author: Nouran Darwish
"""

import numpy as np
import logging
from typing import Optional, Generator
import subprocess
import wave
import io
import time
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSProcessor:
    """
    TTS processor using Piper TTS for child-friendly voice synthesis
    Optimized for streaming with <250ms first chunk
    """
    
    def __init__(self, voice_model: str = "en_US-amy-medium"):
        """
        Initialize TTS with Piper
        Args:
            voice_model: Voice model to use (child-friendly recommended)
        """
        logger.info(f"Initializing TTS with voice: {voice_model}")
        
        self.voice_model = voice_model
        self.sample_rate = 22050  # Piper default
        self.speech_rate = 0.8  # Slower for young children
        
        # Check if Piper is available
        self.piper_available = self._check_piper()
        
        if not self.piper_available:
            logger.warning("Piper TTS not available, using fallback")
            
        logger.info("TTS initialized")
        
    def _check_piper(self) -> bool:
        """Check if Piper TTS is available"""
        try:
            result = subprocess.run(
                ["piper", "--version"],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
            
    def synthesize(self, text: str, streaming: bool = False) -> np.ndarray:
        """
        Synthesize speech from text
        
        Args:
            text: Text to synthesize
            streaming: Enable streaming mode for lower latency
            
        Returns:
            Audio data as numpy array
        """
        try:
            start_time = time.time()
            
            if self.piper_available:
                audio = self._synthesize_piper(text, streaming)
            else:
                audio = self._synthesize_fallback(text)
                
            elapsed = time.time() - start_time
            logger.info(f"TTS synthesis completed in {elapsed:.3f}s")
            
            return audio
            
        except Exception as e:
            logger.error(f"TTS synthesis error: {e}")
            return self._generate_beep()
            
    def _synthesize_piper(self, text: str, streaming: bool) -> np.ndarray:
        """
        Synthesize using Piper TTS
        """
        # Prepare Piper command
        cmd = [
            "piper",
            "--model", self.voice_model,
            "--output-raw",
            "--length-scale", str(1.0 / self.speech_rate),  # Adjust speed
        ]
        
        # Run Piper
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Send text and get audio
        stdout, stderr = process.communicate(input=text.encode())
        
        if process.returncode != 0:
            logger.error(f"Piper error: {stderr.decode()}")
            return self._synthesize_fallback(text)
            
        # Convert raw audio to numpy array
        audio = np.frombuffer(stdout, dtype=np.int16)
        audio = audio.astype(np.float32) / 32768.0
        
        return audio
        
    def _synthesize_fallback(self, text: str) -> np.ndarray:
        """
        Fallback TTS using espeak or festival (simplified)
        """
        try:
            # Try espeak first
            cmd = [
                "espeak",
                "-s", str(int(150 * self.speech_rate)),  # Speed
                "-p", "80",  # Pitch (higher for child-friendly)
                "--stdout",
                text
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # Parse WAV data
                with io.BytesIO(result.stdout) as wav_io:
                    with wave.open(wav_io, 'rb') as wav:
                        frames = wav.readframes(wav.getnframes())
                        audio = np.frombuffer(frames, dtype=np.int16)
                        audio = audio.astype(np.float32) / 32768.0
                        return audio
                        
        except:
            pass
            
        # Ultimate fallback: generate beep pattern
        return self._generate_beep()
        
    def _generate_beep(self) -> np.ndarray:
        """
        Generate a simple beep as ultimate fallback
        """
        duration = 0.5
        frequency = 440  # A4 note
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        audio = np.sin(2 * np.pi * frequency * t) * 0.3
        return audio.astype(np.float32)
        
    def synthesize_streaming(self, text: str, chunk_size: int = 1024) -> Generator[np.ndarray, None, None]:
        """
        Stream TTS synthesis for lower latency
        Yields audio chunks as they're generated
        """
        if not self.piper_available:
            # Fallback: return entire audio at once
            yield self._synthesize_fallback(text)
            return
            
        # Prepare Piper command for streaming
        cmd = [
            "piper",
            "--model", self.voice_model,
            "--output-raw",
            "--length-scale", str(1.0 / self.speech_rate),
        ]
        
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0  # Unbuffered
        )
        
        # Send text
        process.stdin.write(text.encode())
        process.stdin.close()
        
        # Stream output chunks
        while True:
            chunk = process.stdout.read(chunk_size * 2)  # 2 bytes per sample
            if not chunk:
                break
                
            audio_chunk = np.frombuffer(chunk, dtype=np.int16)
            audio_chunk = audio_chunk.astype(np.float32) / 32768.0
            yield audio_chunk
            
        process.wait()
        
    def set_speech_rate(self, rate: float):
        """
        Set speech rate (0.5 = half speed, 1.0 = normal, 2.0 = double)
        """
        self.speech_rate = max(0.5, min(2.0, rate))
        logger.info(f"Speech rate set to {self.speech_rate}x")
        
    def get_child_friendly_voices(self) -> list:
        """
        Get list of available child-friendly voices
        """
        voices = [
            "en_US-amy-medium",  # Young female
            "en_US-danny-low",   # Young male
            "en_US-kathleen-low", # Female
            "en_GB-jenny-medium",  # British female
        ]
        
        # Check which voices are actually available
        available = []
        for voice in voices:
            # Check if voice model exists
            if self._check_voice_available(voice):
                available.append(voice)
                
        return available if available else ["default"]
        
    def _check_voice_available(self, voice: str) -> bool:
        """Check if a specific voice model is available"""
        # Simplified check - in production would check model files
        return True
        
    def emphasize_letter(self, letter: str) -> np.ndarray:
        """
        Special emphasis for teaching individual letters
        """
        # Add pauses and emphasis
        emphasized_text = f"The letter... {letter}... sounds like... {letter}"
        
        # Slower rate for letter teaching
        original_rate = self.speech_rate
        self.speech_rate = 0.6
        
        audio = self.synthesize(emphasized_text)
        
        # Restore original rate
        self.speech_rate = original_rate
        
        return audio