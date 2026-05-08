import cv2
import numpy as np
from PIL import Image, ImageEnhance
from app.core.logger import logger


class ImagePreprocessor:
    """Image preprocessing for OCR"""

    @staticmethod
    def preprocess(image_path: str) -> np.ndarray:
        """
        Comprehensive preprocessing pipeline

        Args:
            image_path: Path to image file

        Returns:
            Preprocessed image as numpy array
        """
        logger.info(f"Starting preprocessing for {image_path}")

        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")

        # Step 1: Auto-rotate if needed
        image = ImagePreprocessor.auto_rotate(image)
        logger.info("Auto-rotation completed")

        # Step 2: Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        logger.info("Converted to grayscale")

        # Step 3: Denoise
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        logger.info("Denoising completed")

        # Step 4: Enhance contrast
        enhanced = ImagePreprocessor.enhance_contrast(denoised)
        logger.info("Contrast enhancement completed")

        # Step 5: Binarization (convert to black and white)
        binary = cv2.threshold(enhanced, 150, 255, cv2.THRESH_BINARY)[1]
        logger.info("Binarization completed")

        # Step 6: Dilation and Erosion to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        logger.info("Morphological operations completed")

        logger.info("Preprocessing pipeline completed successfully")
        return processed

    @staticmethod
    def auto_rotate(image: np.ndarray) -> np.ndarray:
        """
        Auto-detect and rotate image if needed

        Args:
            image: Input image

        Returns:
            Rotated image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 100, 200)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # Find largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(largest_contour)
            angle = rect[2]

            # Rotate if angle is significant
            if angle < -45:
                angle = 90 + angle

            if abs(angle) > 5:  # Only rotate if angle > 5 degrees
                h, w = image.shape[:2]
                center = (w // 2, h // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
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

    @staticmethod
    def enhance_contrast(image: np.ndarray) -> np.ndarray:
        """
        Enhance image contrast and brightness

        Args:
            image: Input grayscale image

        Returns:
            Enhanced image
        """
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)

        # Apply morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        enhanced = cv2.morphologyEx(enhanced, cv2.MORPH_CLOSE, kernel)

        return enhanced

    @staticmethod
    def save_preprocessed_image(image: np.ndarray, output_path: str) -> None:
        """Save preprocessed image for debugging"""
        cv2.imwrite(output_path, image)
        logger.info(f"Preprocessed image saved to {output_path}")
