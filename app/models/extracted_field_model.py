from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.base import Base


class ExtractedFieldModel(Base):

    __tablename__ = "extracted_fields"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    field_name = Column(String)

    field_value = Column(String)
