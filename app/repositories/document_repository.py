from app.models.document_model import DocumentModel


class DocumentRepository:

    def create(
        self,
        db,
        filename,
        document_type,
        confidence,
        raw_text
    ):

        document = DocumentModel(
            filename=filename,
            document_type=document_type,
            confidence=confidence,
            raw_text=raw_text
        )

        db.add(document)

        db.commit()

        db.refresh(document)

        return document
