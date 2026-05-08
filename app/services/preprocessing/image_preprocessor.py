import cv2
import numpy as np

from app.services.preprocessing.base_preprocessor import (
    BasePreprocessor
)
from app.core.logger import logger


class ImagePreprocessor(BasePreprocessor):
    """Advanced image preprocessing for OCR"""

    def preprocess(self, file_path: str) -> np.ndarray:
        """
        Full preprocessing pipeline for document images
        
        Args:
            file_path: Path to input image
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            logger.info(f"Starting preprocessing for {file_path}")
            
            # Read image
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError(f"Could not read image: {file_path}")
            
            # Convert to grayscale
            gray = self._to_grayscale(image)
            logger.info("Converted to grayscale")
            
            # Resize for better OCR readability
            resized = self._resize_image(gray)
            logger.info("Image resized (2x upscaling)")
            
            # Denoise
            denoised = self._denoise(resized)
            logger.info("Denoising completed")
            
            # Rotation correction
            deskewed = self._deskew(denoised)
            logger.info("Deskewing completed")
            
            # Adaptive thresholding for uneven lighting
            thresholded = self._threshold(deskewed)
            logger.info("Thresholding completed")
            
            # Morphological operations for cleanup
            cleaned = self._morphological_cleanup(thresholded)
            logger.info("Morphological cleanup completed")
            
            logger.info("Preprocessing pipeline completed successfully")
            return cleaned
            
        except Exception as e:
            logger.error(f"Preprocessing failed: {str(e)}")
            raise

    def _to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert BGR to grayscale"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def _resize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Resize image for better OCR
        2x upscaling improves tesseract accuracy significantly
        """
        return cv2.resize(
            image,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

    def _denoise(self, image: np.ndarray) -> np.ndarray:
        """Remove noise from image"""
        return cv2.fastNlMeansDenoising(
            image,
            h=10,
            templateWindowSize=7,
            searchWindowSize=21
        )

    def _deskew(self, image: np.ndarray) -> np.ndarray:
        """
        Detect and correct image rotation
        Critical for tilted document uploads
        """
        try:
            # Binary threshold for contour detection
            _, binary = cv2.threshold(
                image,
                150,
                255,
                cv2.THRESH_BINARY
            )
            
            # Find contours
            contours, _ = cv2.findContours(
                binary,
                cv2.RETR_LIST,
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            if len(contours) == 0:
                return image
            
            # Find largest contour
            largest_contour = max(
                contours,
                key=cv2.contourArea
            )
            
            # Calculate rotation angle
            rect = cv2.minAreaRect(largest_contour)
            angle = rect[2]
            
            # Normalize angle
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
            
            # Only rotate if angle is significant
            if abs(angle) > 2:
                h, w = image.shape[:2]
                center = (w // 2, h // 2)
                
                # Get rotation matrix
                rotation_matrix = cv2.getRotationMatrix2D(
                    center,
                    angle,
                    1.0
                )
                
                # Apply rotation
                rotated = cv2.warpAffine(
                    image,
                    rotation_matrix,
                    (w, h),
                    flags=cv2.INTER_CUBIC,
                    borderMode=cv2.BORDER_REPLICATE
                )
                
                logger.info(f"Image rotated by {angle} degrees")
                return rotated
            
            return image
            
        except Exception as e:
            logger.warning(f"Deskewing failed: {str(e)}, continuing without rotation correction")
            return image

    def _threshold(self, image: np.ndarray) -> np.ndarray:
        """
        Apply adaptive thresholding for text
        Better than simple thresholding for uneven lighting
        """
        # Adaptive thresholding works better for documents with uneven lighting
        adaptive = cv2.adaptiveThreshold(
            image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )
        
        return adaptive

    def _morphological_cleanup(
        self,
        image: np.ndarray
    ) -> np.ndarray:
        """
        Remove noise using morphological operations
        Cleans up artifacts while preserving text
        """
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (2, 2)
        )
        
        # Close operation removes small holes in text
        closed = cv2.morphologyEx(
            image,
            cv2.MORPH_CLOSE,
            kernel,
            iterations=1
        )
        
        # Open operation removes small noise
        opened = cv2.morphologyEx(
            closed,
            cv2.MORPH_OPEN,
            kernel,
            iterations=1
        )
        
        return opened
