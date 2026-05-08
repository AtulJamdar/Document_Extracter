from dependency_injector import containers, providers

from app.core.config import settings
from app.services.ocr.tesseract_ocr_service import (
    TesseractOCRService
)
from app.documents.classifiers.keyword_classifier import (
    KeywordClassifier
)
from app.repositories.document_repository import (
    DocumentRepository
)
from app.repositories.extracted_field_repository import (
    ExtractedFieldRepository
)
from app.services.llm.groq_llm_service import (
    GroqLLMService
)


class Container(containers.DeclarativeContainer):

    # OCR Service - configurable based on settings
    if settings.OCR_ENGINE == "tesseract":
        ocr_provider = TesseractOCRService
    else:
        ocr_provider = TesseractOCRService

    ocr_service = providers.Singleton(
        ocr_provider
    )

    # Classifier
    classifier = providers.Singleton(
        KeywordClassifier
    )

    # LLM Service
    llm_service = providers.Singleton(
        GroqLLMService
    )

    # Repositories
    document_repository = providers.Singleton(
        DocumentRepository
    )

    extracted_field_repository = providers.Singleton(
        ExtractedFieldRepository
    )
