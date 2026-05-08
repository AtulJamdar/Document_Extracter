from sqlalchemy import Column, Integer, String, Text, Float

from app.database.base import Base


class DocumentModel(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    document_type = Column(String, nullable=False)

    confidence = Column(Float)

    raw_text = Column(Text)
