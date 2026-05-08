from app.documents.classifiers.base_classifier import BaseClassifier
from app.documents.enums.document_type import DocumentType
from app.documents.schemas.classification_result import ClassificationResult


class KeywordClassifier(BaseClassifier):

    def classify(self, text: str) -> ClassificationResult:

        normalized_text = text.lower()

        # Aadhaar
        if (
            "government of india" in normalized_text
            or "aadhaar" in normalized_text
            or "uidai" in normalized_text
        ):
            return ClassificationResult(
                document_type=DocumentType.AADHAAR,
                confidence=0.95
            )

        # Passport
        if (
            "passport" in normalized_text
            or "republic of india" in normalized_text
        ):
            return ClassificationResult(
                document_type=DocumentType.PASSPORT,
                confidence=0.90
            )

        # Driving License
        if (
            "driving licence" in normalized_text
            or "driving license" in normalized_text
        ):
            return ClassificationResult(
                document_type=DocumentType.DRIVING_LICENSE,
                confidence=0.88
            )

        # Invoice
        if (
            "invoice no" in normalized_text
            or "invoice number" in normalized_text
            or "gst" in normalized_text
        ):
            return ClassificationResult(
                document_type=DocumentType.INVOICE,
                confidence=0.85
            )

        return ClassificationResult(
            document_type=DocumentType.UNKNOWN,
            confidence=0.0
        )
