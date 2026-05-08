# Intelligent Document Extraction Platform

A Python-based intelligent document extraction platform that processes uploaded documents using OCR, image preprocessing, and LLM-assisted extraction.

The system supports structured extraction from multiple document types such as Aadhaar Cards, Passports, Driving Licences, and Invoices using a hybrid extraction pipeline (Regex + LLM).

---

# Features

- OCR-based document text extraction
- OpenCV image preprocessing pipeline
- Hybrid extraction using Regex + Groq LLM
- Template-based document extraction
- Support for multiple document types:
  - Aadhaar Card
  - Passport
  - Driving Licence
  - Invoice
- PostgreSQL database integration
- SQLAlchemy ORM
- Repository Pattern implementation
- Dependency Injection architecture
- Config-driven application setup
- Structured logging using Loguru
- Global exception handling
- Streamlit dashboard UI
- FastAPI backend APIs
- Configurable OCR preprocessing
- Pydantic validation
- Alembic database migrations

---

# Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| OCR | Tesseract OCR |
| LLM | Groq API |
| Image Processing | OpenCV |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Frontend UI | Streamlit |
| Logging | Loguru |
| Validation | Pydantic |
| Dependency Injection | dependency-injector |
| Config Management | pydantic-settings |
| Database Migration | Alembic |
| Testing | Pytest |

---

# Project Architecture

```text
Client (Streamlit UI)
        ↓
FastAPI Backend
        ↓
Image Preprocessing (OpenCV)
        ↓
OCR Engine (Tesseract)
        ↓
Document Classification
        ↓
Regex-Based Extraction
        ↓
LLM Fallback Extraction (Groq)
        ↓
Validation Layer
        ↓
PostgreSQL Database
