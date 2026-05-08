from pydantic import BaseModel

from app.documents.enums.document_type import DocumentType


class ClassificationResult(BaseModel):

    document_type: DocumentType

    confidence: float
