from fastapi import FastAPI

from app.api.routes.document_routes import router
from app.core.handlers import (
    ocr_exception_handler,
    extraction_exception_handler,
    validation_exception_handler
)
from app.core.exceptions import (
    OCRException,
    ExtractionException,
    ValidationException
)
from app.core.config import settings
from app.core.logger import logger


app = FastAPI(title=settings.APP_NAME)

logger.info(f"Starting {settings.APP_NAME}")
logger.info(f"Database: {settings.DATABASE_URL}")
logger.info(f"OCR Engine: {settings.OCR_ENGINE}")

app.add_exception_handler(
    OCRException,
    ocr_exception_handler
)

app.add_exception_handler(
    ExtractionException,
    extraction_exception_handler
)

app.add_exception_handler(
    ValidationException,
    validation_exception_handler
)

app.include_router(router)