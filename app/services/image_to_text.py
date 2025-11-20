"""
Image-to-text service using PaddleOCR
"""
import logging
from pathlib import Path
from typing import List, Tuple
from app.models.job import BoundingBox
import cv2
import numpy as np

logger = logging.getLogger(__name__)

class ImageToTextService:
    """Service for extracting text from images"""
    
    def __init__(self):
        self.initialized = False
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize PaddleOCR model"""
        try:
            from paddleocr import PaddleOCR
            self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
            self.initialized = True
            logger.info("PaddleOCR model initialized")
        except Exception as e:
            logger.warning(f"PaddleOCR not available: {e}. Using fallback.")
            self.ocr = None
    
    def extract_text(self, file_path: str) -> Tuple[str, List[BoundingBox]]:
        """
        Extract text from image
        
        Args:
            file_path: Path to image file
            
        Returns:
            Tuple of (full_text, bounding_boxes)
        """
        if not self.initialized or self.ocr is None:
            return self._mock_extract(file_path)
        
        try:
            logger.info(f"Starting OCR for: {file_path}")
            
            result = self.ocr.ocr(file_path, cls=True)
            
            bboxes = []
            texts = []
            
            if result and len(result) > 0:
                for line in result:
                    for word_info in line:
                        points = word_info[0]
                        text = word_info[1][0]
                        confidence = word_info[1][1]
                        
                        # Calculate bounding box from points
                        x_coords = [p[0] for p in points]
                        y_coords = [p[1] for p in points]
                        
                        x = min(x_coords)
                        y = min(y_coords)
                        width = max(x_coords) - x
                        height = max(y_coords) - y
                        
                        bbox = BoundingBox(
                            x=float(x), y=float(y),
                            width=float(width), height=float(height),
                            text=text, confidence=float(confidence)
                        )
                        bboxes.append(bbox)
                        texts.append(text)
            
            full_text = " ".join(texts)
            logger.info(f"Extracted {len(bboxes)} text regions")
            
            return full_text, bboxes
            
        except Exception as e:
            logger.error(f"Error in OCR: {e}")
            raise
    
    def _mock_extract(self, file_path: str) -> Tuple[str, List[BoundingBox]]:
        """Mock implementation"""
        mock_text = "Sample text from image"
        bboxes = [
            BoundingBox(x=10, y=10, width=100, height=30, text="Sample", confidence=0.95),
            BoundingBox(x=120, y=10, width=80, height=30, text="text", confidence=0.93),
            BoundingBox(x=210, y=10, width=100, height=30, text="from", confidence=0.92),
            BoundingBox(x=320, y=10, width=100, height=30, text="image", confidence=0.94),
        ]
        return mock_text, bboxes


class MockImageToTextService:
    """Mock OCR service for development"""
    
    def extract_text(self, file_path: str) -> Tuple[str, List[BoundingBox]]:
        """Return mock OCR results"""
        mock_text = "Extracted text from image sample"
        bboxes = [
            BoundingBox(x=50, y=50, width=150, height=40, text="Extracted text", confidence=0.98),
            BoundingBox(x=50, y=100, width=150, height=40, text="from image", confidence=0.97),
        ]
        return mock_text, bboxes
