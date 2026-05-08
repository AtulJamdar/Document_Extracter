# 📄 Document Extraction Platform - Streamlit UI

A practical, production-grade frontend for the intelligent document extraction backend.

## Features

✅ **Document Upload** - Drag-and-drop PNG/JPG/JPEG support
✅ **Live Preview** - See uploaded images before processing
✅ **Fast Extraction** - Call backend API and display results instantly
✅ **Structured Data** - View extracted fields organized by type
✅ **Confidence Scores** - Know how confident the extraction is
✅ **Raw OCR Text** - Debug OCR quality with raw text display
✅ **Extraction History** - Track all extractions with timestamps
✅ **Error Handling** - Graceful error messages for all failure cases
✅ **Debug Mode** - Toggle debug information for development

## Architecture

```
streamlit_ui/
├── app.py              ← Main Streamlit application
├── api_client.py       ← Centralized API communication (NO business logic)
├── components/         ← Reusable UI components (optional)
├── requirements.txt    ← UI dependencies
└── __init__.py         ← Package marker
```

### Design Principles

**IMPORTANT:** This is a FRONTEND ONLY module.

- ✅ **All business logic in backend** - Extraction, classification, preprocessing
- ✅ **Centralized API calls** - api_client.py handles all communication
- ✅ **Graceful error handling** - Backend errors displayed nicely to users
- ✅ **Debug-friendly** - Raw OCR text and full responses for troubleshooting
- ✅ **Session state** - Streamlit session_state for history and current results
- ✅ **No hardcoded logic** - All configuration in backend

## Quick Start

### 1. Install Dependencies

```bash
pip install -r streamlit_ui/requirements.txt
```

Or manually:
```bash
pip install streamlit requests pandas
```

### 2. Ensure Backend is Running

```bash
# Terminal 1 - Start FastAPI backend
uvicorn app.main:app --reload
# Server runs at http://127.0.0.1:8000
```

### 3. Start Streamlit UI

```bash
# Terminal 2 - Start Streamlit
streamlit run streamlit_ui/app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

A browser will automatically open to the dashboard.

### 4. Test the Pipeline

1. Click "Choose a document image"
2. Upload a PNG/JPG of Aadhaar, Passport, Driving License, or Invoice
3. Click "Extract Information"
4. View extracted data in tabs

## UI Components

### Upload Section
- File uploader (PNG/JPG/JPEG)
- Image preview
- Extract button

### Results Tabs

#### 📊 Extracted Data Tab
- Document type and confidence score
- Extracted fields as form inputs (read-only)
- Download as JSON button

#### 📝 OCR Text Tab
- Raw text from Tesseract
- Character and line counts
- Used for debugging extraction failures

#### 📈 Metadata Tab
- Document ID
- Document type
- Confidence score
- Extraction timestamp
- Filename

#### 🔍 Debug Tab
- Toggle via sidebar checkbox
- Full API response JSON
- Processing notes

### Extraction History
- Table showing all extractions
- Timestamp, filename, type, confidence, status
- Clear history button

## Error Handling

The UI gracefully handles these backend errors:

```
❌ Connection refused
   → "Cannot connect to backend. Is the server running?"

❌ Invalid file type
   → Displays backend error message

❌ OCR failure
   → Shows error with raw response

❌ Timeout
   → "Request timeout. Backend is not responding."
```

## Configuration

### Sidebar Settings

**Backend URL**
```python
Default: http://127.0.0.1:8000
Change if backend runs on different host
```

**Show Debug Information**
```python
Default: False
Enable to see full API responses and processing details
```

## API Response Format

The API returns this format:

```json
{
  "document_id": 123,
  "document_type": "aadhaar",
  "confidence": 0.95,
  "raw_text": "Raw OCR output here...",
  "extracted_data": {
    "aadhaar_number": "1234 5678 9012",
    "name": "John Doe",
    "dob": "01/01/1990"
  }
}
```

Or on error:
```json
{
  "error": {
    "message": "Invalid file type",
    "code": 400
  }
}
```

## Session State

Streamlit uses session_state to persist:

- `extraction_history` - List of all extractions
- `current_result` - Last extraction result
- `uploaded_file_bytes` - Current file being processed

This allows history to persist across reruns.

## Development

### Adding New UI Features

1. **Never add business logic** - Keep all logic in backend
2. **Update api_client.py** - For new API endpoints
3. **Use components/** - For reusable UI pieces
4. **Test with backend** - Always verify backend is running

### Testing the API Client

```python
from streamlit_ui.api_client import api_client

# Test upload
with open("test_image.jpg", "rb") as f:
    result = api_client.upload_document(f.read(), "test_image.jpg")
    print(result)
```

### Common Issues

**Issue: "Cannot connect to backend"**
```
Solution: Ensure FastAPI server is running
$ uvicorn app.main:app --reload
```

**Issue: "No extracted data displayed"**
```
Solution: Check OCR Text tab for raw extraction
Backend may have failed extraction (show debug info)
```

**Issue: Slow extraction**
```
Solution: Check if preprocessing is enabled
Disable preprocessing in backend config if too slow
```

## Performance

- **Upload handling**: 0.1s (file validation)
- **API call**: 2-5s (OCR + extraction)
- **Display**: 0.1s (UI rendering)

**Total time: ~3-6 seconds per document**

## Deployment

### Local Network Testing
```bash
streamlit run streamlit_ui/app.py \
  --server.port 8501 \
  --server.address 0.0.0.0
```

Then access from other computers:
```
http://<your_ip>:8501
```

### Production Considerations
- Use nginx reverse proxy
- Enable HTTPS
- Add authentication
- Use production database backend
- Configure CORS properly
- Rate limit API calls
- Add request logging

## Next Steps

### Optional Enhancements

1. **Multi-file batch upload**
   ```python
   uploaded_files = st.file_uploader(..., accept_multiple_files=True)
   ```

2. **Document-specific templates**
   ```python
   if document_type == "aadhaar":
       display_aadhaar_template()
   ```

3. **Export results**
   - Download as CSV
   - Download as PDF
   - Email extracted data

4. **Backend integration for history**
   - Query GET /documents endpoint
   - Show database extraction history
   - Not just session history

5. **Performance metrics**
   - OCR processing time
   - API response time
   - Extraction accuracy over time

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│           STREAMLIT UI (Frontend)               │
│  - Upload, Preview, Display, History, Settings  │
└──────────────────┬──────────────────────────────┘
                   │
                   │ HTTP REST API
                   │ POST /extract-text
                   │
┌──────────────────▼──────────────────────────────┐
│    FASTAPI BACKEND (Business Logic)             │
│  - File validation, OCR, Classification         │
│  - Extraction, Database, Error handling         │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
    ┌───▼──┐  ┌───▼──┐  ┌──▼────┐
    │  OCR │  │ Class│  │Extract│
    │Engine│  │ifier │  │Engine │
    └───┬──┘  └───┬──┘  └──┬────┘
        │         │        │
    ┌───▼─────────▼────────▼────┐
    │   Database (PostgreSQL)    │
    │ Extraction Results History │
    └────────────────────────────┘
```

## Troubleshooting

### Everything works locally but doesn't start?
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r streamlit_ui/requirements.txt --force-reinstall

# Run with verbose output
streamlit run streamlit_ui/app.py --logger.level=debug
```

### Backend connection issues?
```bash
# Test API directly
curl -X POST http://127.0.0.1:8000/extract-text -F "file=@test.jpg"

# Check backend is listening
netstat -an | findstr :8000
```

### Slow performance?
```python
# In backend .env
ENABLE_PREPROCESSING=false  # Speed up initial test
# Then enable after verifying basic flow works
```

## Files Modified

- `streamlit_ui/app.py` - Main UI application
- `streamlit_ui/api_client.py` - API communication layer
- `app/api/routes/document_routes.py` - Enhanced API response

## File Structure

```
streamlit_ui/
├── app.py                    ← Main Streamlit app (START HERE)
├── api_client.py             ← API communication (DO NOT modify endpoints lightly)
├── components/               ← Future reusable components
├── __init__.py               ← Package marker
└── requirements.txt          ← Dependencies

.streamlit/
└── config.toml               ← Streamlit configuration
```

---

**Remember:** This is an engineering tool, not a design showcase.
Focus on functionality, clarity, and debug-friendliness. ✅
