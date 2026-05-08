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


app = FastAPI()

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