import pytesseract
from PIL import Image
import cv2

from app.services.ocr.base_ocr import BaseOCRService
from app.services.preprocessing.image_preprocessor import ImagePreprocessor
from app.core.logger import logger
from app.core.decorators import log_execution
from app.core.exceptions import OCRException


class TesseractOCRService(BaseOCRService):

    @log_execution
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from image with preprocessing

        Args:
            file_path: Path to image file

        Returns:
            Extracted text
        """
        try:
            # Preprocess image
            preprocessed_image = ImagePreprocessor.preprocess(file_path)

            # Convert numpy array to PIL Image for pytesseract
            pil_image = Image.fromarray(preprocessed_image)

            # Extract text using Tesseract
            text = pytesseract.image_to_string(pil_image)

            return text

        except Exception as e:
            raise OCRException(
                f"OCR processing failed: {str(e)}"
            )