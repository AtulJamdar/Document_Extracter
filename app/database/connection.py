from sqlalchemy import create_engine


# IMPORTANT: Replace with your actual PostgreSQL credentials
# Format: postgresql://username:password@localhost/database_name
DATABASE_URL = (
    "postgresql://postgres:%40atul123@localhost/doc_db"
)

engine = create_engine(DATABASE_URL)
