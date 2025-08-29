"""
Object Detection Module
Uses YOLOv8n for detecting objects mapped to letters
Author: Nouran Darwish
"""

import cv2
import numpy as np
from typing import Dict, List, Optional
import logging
import json

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ObjectDetector:
    """
    Detects objects that map to alphabet letters
    Uses YOLOv8n for efficient object detection
    """
    
    def __init__(self):
        """Initialize object detector"""
        logger.info("Initializing Object Detector")
        
        # Object to letter mapping
        self.object_letter_map = {
            'apple': 'A',
            'ball': 'B', 'sports ball': 'B',
            'cat': 'C',
            'dog': 'D',
            'elephant': 'E',
            'fish': 'F',
            'grapes': 'G',
            'hat': 'H',
            'ice cream': 'I',
            'jacket': 'J',
            'kite': 'K',
            'lion': 'L',
            'mouse': 'M',
            'nest': 'N',
            'orange': 'O',
            'penguin': 'P',
            'queen': 'Q',
            'robot': 'R',
            'sun': 'S',
            'tree': 'T',
            'umbrella': 'U',
            'van': 'V', 'truck': 'V',
            'window': 'W',
            'x-ray': 'X',
            'yo-yo': 'Y',
            'zebra': 'Z'
        }
        
        # Initialize YOLO if available
        if YOLO_AVAILABLE:
            try:
                self.model = YOLO('yolov8n.pt')
                self.yolo_available = True
                logger.info("YOLOv8n loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load YOLO: {e}")
                self.yolo_available = False
        else:
            logger.warning("YOLO not available, using fallback")
            self.yolo_available = False
            
    def detect(self, image: np.ndarray, confidence_threshold: float = 0.5) -> Dict:
        """
        Detect objects in image that map to letters
        
        Args:
            image: Input image as numpy array
            confidence_threshold: Minimum confidence for detection
            
        Returns:
            Dictionary with detection results
        """
        try:
            if self.yolo_available:
                return self._detect_yolo(image, confidence_threshold)
            else:
                return self._detect_fallback(image)
                
        except Exception as e:
            logger.error(f"Object detection error: {e}")
            return {"detected": False, "error": str(e)}
            
    def _detect_yolo(self, image: np.ndarray, confidence_threshold: float) -> Dict:
        """
        Detect objects using YOLOv8
        """
        # Run inference
        results = self.model(image, conf=confidence_threshold)
        
        detections = []
        
        for r in results:
            if r.boxes is not None:
                for box in r.boxes:
                    # Get class name
                    class_id = int(box.cls)
                    class_name = self.model.names[class_id].lower()
                    confidence = float(box.conf)
                    
                    # Check if object maps to a letter
                    letter = self._get_letter_for_object(class_name)
                    
                    if letter:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        detections.append({
                            'label': class_name,
                            'letter': letter,
                            'confidence': confidence,
                            'bbox': [int(x1), int(y1), int(x2), int(y2)]
                        })
                        
        if detections:
            # Sort by confidence
            detections.sort(key=lambda x: x['confidence'], reverse=True)
            
            return {
                'detected': True,
                'objects': detections,
                'count': len(detections),
                'primary_object': detections[0]['label'],
                'primary_letter': detections[0]['letter']
            }
        else:
            return {
                'detected': False,
                'message': 'No alphabet-related objects found'
            }
            
    def _detect_fallback(self, image: np.ndarray) -> Dict:
        """
        Fallback detection using basic computer vision
        """
        # Convert to HSV for color-based detection
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        detections = []
        
        # Detect specific objects by color/shape
        # This is a simplified approach
        
        # Example: Detect ball (circular objects)
        circles = self._detect_circles(image)
        if circles:
            detections.append({
                'label': 'ball',
                'letter': 'B',
                'confidence': 0.6,
                'bbox': circles[0]
            })
            
        # Example: Detect apple (red circular objects)
        red_objects = self._detect_color_objects(hsv, 'red')
        for obj in red_objects:
            if self._is_circular(obj):
                detections.append({
                    'label': 'apple',
                    'letter': 'A',
                    'confidence': 0.5,
                    'bbox': obj
                })
                break
                
        if detections:
            return {
                'detected': True,
                'objects': detections,
                'count': len(detections),
                'primary_object': detections[0]['label'],
                'primary_letter': detections[0]['letter']
            }
        else:
            return {
                'detected': False,
                'message': 'No objects detected (fallback mode)'
            }
            
    def _get_letter_for_object(self, object_name: str) -> Optional[str]:
        """
        Get the letter that corresponds to an object
        """
        object_lower = object_name.lower()
        
        # Direct match
        if object_lower in self.object_letter_map:
            return self.object_letter_map[object_lower]
            
        # Partial match
        for key, letter in self.object_letter_map.items():
            if key in object_lower or object_lower in key:
                return letter
                
        # Common COCO classes to letter mapping
        coco_map = {
            'person': 'P',
            'bicycle': 'B',
            'car': 'C',
            'airplane': 'A',
            'bird': 'B',
            'boat': 'B',
            'bottle': 'B',
            'chair': 'C',
            'cow': 'C',
            'dining table': 'T',
            'horse': 'H',
            'sheep': 'S',
            'train': 'T',
            'tv': 'T',
            'laptop': 'L',
            'keyboard': 'K',
            'book': 'B',
            'clock': 'C',
            'scissors': 'S',
            'teddy bear': 'T',
            'hair drier': 'H',
            'toothbrush': 'T'
        }
        
        if object_lower in coco_map:
            return coco_map[object_lower]
            
        return None
        
    def _detect_circles(self, image: np.ndarray) -> List:
        """
        Detect circular objects (simplified)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=50,
            param1=50,
            param2=30,
            minRadius=20,
            maxRadius=200
        )
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            result = []
            for (x, y, r) in circles:
                result.append([x-r, y-r, x+r, y+r])
            return result
        return []
        
    def _detect_color_objects(self, hsv: np.ndarray, color: str) -> List:
        """
        Detect objects of specific color
        """
        # Define color ranges in HSV
        color_ranges = {
            'red': [(0, 100, 100), (10, 255, 255)],
            'green': [(35, 100, 100), (85, 255, 255)],
            'blue': [(100, 100, 100), (130, 255, 255)],
            'yellow': [(20, 100, 100), (35, 255, 255)]
        }
        
        if color not in color_ranges:
            return []
            
        lower, upper = color_ranges[color]
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        objects = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(contour)
                objects.append([x, y, x+w, y+h])
                
        return objects
        
    def _is_circular(self, bbox: List) -> bool:
        """
        Check if bounding box contains circular object
        """
        x1, y1, x2, y2 = bbox
        w = x2 - x1
        h = y2 - y1
        aspect_ratio = w / h if h > 0 else 0
        
        # Circular objects have aspect ratio close to 1
        return 0.8 < aspect_ratio < 1.2
        
    def get_alphabet_objects(self) -> Dict[str, List[str]]:
        """
        Get all objects mapped to each letter
        """
        letter_objects = {}
        
        for obj, letter in self.object_letter_map.items():
            if letter not in letter_objects:
                letter_objects[letter] = []
            letter_objects[letter].append(obj)
            
        return letter_objects