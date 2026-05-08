from app.models.extracted_field_model import (
    ExtractedFieldModel
)


class ExtractedFieldRepository:

    def create(
        self,
        db,
        document_id,
        field_name,
        field_value
    ):

        field = ExtractedFieldModel(
            document_id=document_id,
            field_name=field_name,
            field_value=str(field_value)
        )

        db.add(field)

        db.commit()

        db.refresh(field)

        return field
