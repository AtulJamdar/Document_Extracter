from app.database.connection import engine
from app.database.base import Base

from app.models.document_model import DocumentModel
from app.models.extracted_field_model import ExtractedFieldModel


Base.metadata.create_all(bind=engine)

print("Tables created successfully")
