"""
Speech processing module for KidSafe Alphabet Tutor
Includes ASR and TTS components
"""

from .asr import ASRProcessor
from .tts import TTSProcessor

__all__ = ['ASRProcessor', 'TTSProcessor']