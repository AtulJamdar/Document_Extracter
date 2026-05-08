from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    OCRException,
    ExtractionException,
    ValidationException
)


async def ocr_exception_handler(
    request: Request,
    exc: OCRException
):

    return JSONResponse(
        status_code=500,
        content={
            "error": "OCR_ERROR",
            "message": exc.message
        }
    )


async def extraction_exception_handler(
    request: Request,
    exc: ExtractionException
):

    return JSONResponse(
        status_code=500,
        content={
            "error": "EXTRACTION_ERROR",
            "message": exc.message
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: ValidationException
):

    return JSONResponse(
        status_code=400,
        content={
            "error": "VALIDATION_ERROR",
            "message": exc.message
        }
    )
