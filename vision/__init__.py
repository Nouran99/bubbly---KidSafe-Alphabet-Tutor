"""
Vision processing module for KidSafe Alphabet Tutor
Includes letter and object detection components
"""

from .letter_detector import LetterDetector
from .object_detector import ObjectDetector

__all__ = ['LetterDetector', 'ObjectDetector']