import pytesseract
from PIL import Image

from app.services.ocr.base_ocr import BaseOCRService
from app.services.preprocessing.image_preprocessor import ImagePreprocessor
from app.core.logger import logger
from app.core.decorators import log_execution
from app.core.exceptions import OCRException
from app.core.config import settings


class TesseractOCRService(BaseOCRService):

    def __init__(self):
        self.preprocessor = ImagePreprocessor()

    @log_execution
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from image with optional preprocessing

        Args:
            file_path: Path to image file

        Returns:
            Extracted text
        """
        try:
            # Check if preprocessing is enabled
            if settings.ENABLE_PREPROCESSING:
                logger.info("Preprocessing enabled")
                preprocessed_image = self.preprocessor.preprocess(file_path)
                pil_image = Image.fromarray(preprocessed_image)
            else:
                logger.info("Preprocessing disabled, using raw image")
                pil_image = Image.open(file_path)

            # Extract text using Tesseract
            text = pytesseract.image_to_string(pil_image)

            return text

        except Exception as e:
            raise OCRException(
                f"OCR processing failed: {str(e)}"
            )