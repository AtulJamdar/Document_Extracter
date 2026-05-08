# 🚀 Quick Start Guide - Document Extraction Platform

> **TL;DR:** Run `run_full_stack.bat` and upload a document. That's it!

---

## ⚡ The Fastest Way to Get Started

### Windows Users
```bash
run_full_stack.bat
```

### Linux/Mac Users
```bash
bash run_full_stack.sh
```

**What happens:**
1. Terminal 1: Backend starts at `http://127.0.0.1:8000`
2. Terminal 2: UI opens at `http://localhost:8501`
3. Browser shows extraction dashboard automatically

---

## 📖 Manual Setup (5 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
pip install -r streamlit_ui/requirements.txt
```

### Step 2: Start Backend (Terminal 1)
```bash
uvicorn app.main:app --reload
```
✅ Backend running at `http://127.0.0.1:8000`

### Step 3: Start Frontend (Terminal 2)
```bash
streamlit run streamlit_ui/app.py
```
✅ UI running at `http://localhost:8501`

### Step 4: Open Browser
The browser should open automatically. If not, visit:
```
http://localhost:8501
```

### Step 5: Upload & Extract
1. Click "Choose a document image"
2. Upload PNG/JPG of: Aadhaar, Passport, Invoice, or Driving License
3. Click "Extract Information"
4. View results!

---

## 🧪 Test with Sample Documents

### Document 1: Aadhaar
- File: Any Aadhaar image
- Expected: Extraction of ID, Name, DOB

### Document 2: Passport
- File: Any Passport image
- Expected: Extraction of ID, Name, Nationality

### Document 3: Invoice
- File: Any Invoice image
- Expected: Extraction of Invoice #, Amount, Date

### Document 4: Driving License
- File: Any DL image
- Expected: Extraction of DL #, Name, DOB

---

## 📊 Understanding the UI

### Upload Section (Top)
- **Left:** Image preview
- **Right:** Extract button

### Results (After Extraction)

**Tab 1: Extracted Data** 📊
```
Document Type: [Shows type]
Confidence: [95%]

[Field 1]: [Value]
[Field 2]: [Value]

[Download JSON]
```

**Tab 2: OCR Text** 📝
```
Raw text from Tesseract OCR
(For debugging extraction quality)
```

**Tab 3: Metadata** 📈
```
Document ID: 123
Type: aadhaar
Confidence: 95%
Timestamp: 2024-05-08 14:30:45
```

**Tab 4: Debug** 🔍
```
(Only if Debug Mode enabled in Settings)
Full API response + processing notes
```

### History (Bottom)
Table showing all extractions with status

---

## ⚙️ Settings (Sidebar)

### Backend URL
```
Default: http://127.0.0.1:8000
Change if backend on different machine
```

### Debug Mode
```
Toggle to see full API responses
Useful for troubleshooting
```

---

## ❌ Troubleshooting

### Issue: "Cannot connect to backend"
```
✅ Solution: 
  1. Ensure backend terminal shows "Uvicorn running"
  2. Check http://127.0.0.1:8000 in browser
  3. If not working, restart backend
```

### Issue: "No extracted data shown"
```
✅ Solution:
  1. Check "OCR Text" tab for raw content
  2. Enable Debug mode to see errors
  3. Verify document is clear/readable
```

### Issue: "File upload fails"
```
✅ Solution:
  1. Ensure file is PNG/JPG/JPEG
  2. File is under 10MB
  3. Image has readable content
```

### Issue: "Backend shows errors"
```
✅ Solution:
  1. Check logs/ directory for detailed logs
  2. Verify .env configuration
  3. Restart the server
```

---

## 📱 Full Workflow

```
1. User Upload File
        ↓
2. Streamlit Preview
        ↓
3. Click "Extract"
        ↓
4. Backend Processing
   ├── OCR (reads text)
   ├── Classification (detects type)
   ├── Extraction (gets fields)
   └── Database Save (stores)
        ↓
5. Streamlit Display Results
   ├── Extracted fields
   ├── Confidence score
   ├── Raw OCR text
   └── Metadata
        ↓
6. User Reviews & Downloads
```

**Total time: 3-6 seconds**

---

## 🔧 Configuration

### Enable/Disable Preprocessing

Edit `.env`:
```
ENABLE_PREPROCESSING=true    # Default (better OCR)
ENABLE_PREPROCESSING=false   # Faster, no preprocessing
```

Restart backend after change.

### Change Database

Edit `.env`:
```
DATABASE_URL=postgresql://user:pass@localhost/doc_db
```

### Change OCR Engine

Edit `.env`:
```
OCR_ENGINE=tesseract    # Only option for now
```

---

## 📚 API Documentation

### Auto-Generated Docs
```
http://127.0.0.1:8000/docs
```

Visit this URL to see:
- Request format
- Response format
- Try it out (test API directly)

---

## 🎯 What Each Document Type Extracts

### Aadhaar
- Aadhaar Number
- Name
- Date of Birth
- Gender
- Address

### Passport
- Passport Number
- Name
- Date of Birth
- Nationality
- Expiry Date

### Driving License
- License Number
- Name
- Date of Birth
- Valid From/To
- Address

### Invoice
- Invoice Number
- Date
- Total Amount
- Customer Name
- Items

---

## 💾 Where Data is Stored

```
Database: PostgreSQL (localhost/doc_db)
Logs: logs/app.log
Uploads: app/uploads/
Temp: app/uploads/temp/
```

To reset:
```bash
# Backup database first!
# Then restart PostgreSQL

# View logs
tail -f logs/app.log
```

---

## 🚨 Important Notes

### ✅ DO
- Upload clear, readable documents
- Use PNG/JPG/JPEG formats
- Keep file under 10MB
- Check OCR text for quality
- Use debug mode for troubleshooting

### ❌ DON'T
- Upload documents that are too blurry
- Use unsupported formats (PDF, BMP)
- Upload files over 10MB
- Modify backend code without understanding it
- Forget to enable preprocessing (it helps!)

---

## 📞 Support

### Quick Links
- **System Overview:** Read `SYSTEM_OVERVIEW.md`
- **Phase 9 Details:** Read `PHASE_9_GUIDE.md`
- **Backend Docs:** Read `app/core/config.py` for config options
- **UI Docs:** Read `streamlit_ui/README.md` for advanced features

### Common Questions

**Q: Can I process multiple files at once?**
A: Not yet. Upload one at a time. Enhancement in Phase 11.

**Q: What if extraction fails?**
A: Check the OCR text. If Tesseract couldn't read it, extraction fails. Improve lighting/focus.

**Q: Can I export results?**
A: Yes! Click "Download as JSON" in Extracted Data tab.

**Q: Is my data private?**
A: It stays in your local database. No external calls except to Groq LLM.

**Q: Can I add new document types?**
A: Yes. Create extractor in `app/documents/extractors/` and add to factory.

---

## ✅ You're Ready!

That's all you need to start extracting documents.

The rest is just exploring what the system can do.

**Questions?** Check the docs. They cover everything.

**Good luck!** 🚀
