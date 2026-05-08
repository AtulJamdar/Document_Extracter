from fastapi import APIRouter, UploadFile, File

from app.utils.file_handler import save_uploaded_file
from app.utils.validators import validate_file_extension
from app.documents.extractors.extractor_factory import ExtractorFactory
from app.database.session import SessionLocal
from app.core.container import Container


router = APIRouter()

container = Container()

ocr_service = container.ocr_service()
classifier = container.classifier()
document_repository = container.document_repository()
field_repository = container.extracted_field_repository()


@router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):

    db = SessionLocal()

    try:

        validate_file_extension(file.filename)

        file_path = save_uploaded_file(file)

        extracted_text = ocr_service.extract_text(file_path)

        classification_result = classifier.classify(
            extracted_text
        )

        extractor = ExtractorFactory.get_extractor(
            classification_result.document_type
        )

        extracted_data = None

        if extractor:
            extracted_data = extractor.extract(
                extracted_text
            )

        saved_document = document_repository.create(
            db=db,
            filename=file.filename,
            document_type=classification_result.document_type,
            confidence=classification_result.confidence,
            raw_text=extracted_text
        )

        if extracted_data:

            for field_name, field_value in (
                extracted_data.model_dump().items()
            ):

                field_repository.create(
                    db=db,
                    document_id=saved_document.id,
                    field_name=field_name,
                    field_value=field_value
                )

        return {
            "document_id": saved_document.id,
            "document_type": classification_result.document_type,
            "confidence": classification_result.confidence,
            "raw_text": extracted_text,
            "extracted_data": extracted_data.model_dump() if extracted_data else {}
        }

    finally:
        db.close()