"""
Letter Detection Module
Uses OpenCV and Tesseract for detecting printed letters A-Z
Author: Nouran Darwish
"""

import cv2
import pytesseract
import numpy as np
from typing import Dict, Optional, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LetterDetector:
    """
    Detects printed capital letters A-Z from images
    Uses OpenCV for preprocessing and Tesseract for OCR
    """
    
    def __init__(self):
        """Initialize letter detector"""
        logger.info("Initializing Letter Detector")
        
        # Tesseract configuration for single character detection
        self.tesseract_config = '--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        # Check Tesseract availability
        try:
            pytesseract.get_tesseract_version()
            self.tesseract_available = True
        except:
            logger.warning("Tesseract not available")
            self.tesseract_available = False
            
    def detect(self, image: np.ndarray) -> Dict:
        """
        Detect letters in image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Dictionary with detection results
        """
        try:
            if not self.tesseract_available:
                return {"detected": False, "error": "Tesseract not available"}
                
            # Preprocess image
            processed = self._preprocess_image(image)
            
            # Find letter regions
            letter_regions = self._find_letter_regions(processed)
            
            if not letter_regions:
                return {
                    "detected": False,
                    "message": "No letters found"
                }
                
            # Detect letters in each region
            detections = []
            for region in letter_regions:
                x, y, w, h = region
                roi = processed[y:y+h, x:x+w]
                
                # OCR on region
                text = pytesseract.image_to_string(roi, config=self.tesseract_config)
                confidence = self._get_confidence(roi)
                
                if text.strip():
                    detections.append({
                        "letter": text.strip()[0],  # Take first character
                        "confidence": confidence,
                        "bbox": region
                    })
                    
            if detections:
                # Return best detection
                best = max(detections, key=lambda x: x['confidence'])
                return {
                    "detected": True,
                    "letter": best['letter'],
                    "confidence": best['confidence'],
                    "bbox": best['bbox'],
                    "all_detections": detections
                }
            else:
                return {
                    "detected": False,
                    "message": "Could not recognize letters"
                }
                
        except Exception as e:
            logger.error(f"Letter detection error: {e}")
            return {"detected": False, "error": str(e)}
            
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image.copy()
            
        # Resize if too small
        if gray.shape[0] < 100 or gray.shape[1] < 100:
            scale = 200 / min(gray.shape)
            new_size = (int(gray.shape[1] * scale), int(gray.shape[0] * scale))
            gray = cv2.resize(gray, new_size, interpolation=cv2.INTER_CUBIC)
            
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        
        # Denoise
        denoised = cv2.medianBlur(binary, 3)
        
        # Morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
        
    def _find_letter_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Find potential letter regions in image
        """
        regions = []
        
        # Find contours
        contours, _ = cv2.findContours(
            image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter contours that could be letters
        img_h, img_w = image.shape
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by size and aspect ratio
            aspect_ratio = w / h if h > 0 else 0
            area_ratio = (w * h) / (img_w * img_h)
            
            # Letters typically have aspect ratio 0.5-2.0
            # and occupy 1-50% of image
            if (0.3 < aspect_ratio < 3.0 and 
                0.01 < area_ratio < 0.5 and
                w > 20 and h > 20):
                regions.append((x, y, w, h))
                
        # Sort by area (largest first)
        regions.sort(key=lambda r: r[2] * r[3], reverse=True)
        
        return regions[:5]  # Return top 5 regions
        
    def _get_confidence(self, roi: np.ndarray) -> float:
        """
        Calculate confidence score for OCR result
        """
        try:
            # Get detailed OCR data
            data = pytesseract.image_to_data(
                roi,
                config=self.tesseract_config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract confidence scores
            confidences = [
                int(conf) / 100.0
                for conf in data['conf']
                if int(conf) > 0
            ]
            
            if confidences:
                return np.mean(confidences)
            else:
                return 0.0
                
        except:
            return 0.5  # Default confidence
            
    def detect_handwritten(self, image: np.ndarray) -> Dict:
        """
        Detect handwritten letters (simplified version)
        Note: Full implementation would use a CNN model
        """
        # For now, use same method as printed
        # In production, would use a trained model for handwriting
        result = self.detect(image)
        
        # Adjust confidence for handwriting
        if result.get('detected'):
            result['confidence'] *= 0.7  # Lower confidence for handwriting
            result['handwritten'] = True
            
        return result