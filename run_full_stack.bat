@echo off
REM Script to run both FastAPI backend and Streamlit UI
REM Usage: run_full_stack.bat

echo ==========================================
echo Document Extraction Platform - Full Stack
echo ==========================================
echo.

REM Check if venv is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo Starting FastAPI Backend...
echo ==========================================
REM Start backend in a new window
start cmd /k "cd /d %cd% && uvicorn app.main:app --reload --log-level info"

timeout /t 3

echo.
echo Starting Streamlit UI...
echo ==========================================
REM Start Streamlit
start cmd /k "cd /d %cd% && streamlit run streamlit_ui\app.py"

echo.
echo ==========================================
echo ✅ Full Stack Started
echo ==========================================
echo.
echo Backend URL:  http://127.0.0.1:8000
echo Backend Docs: http://127.0.0.1:8000/docs
echo Streamlit UI: http://localhost:8501
echo.
echo Close either terminal to stop that service
echo Close both terminals to stop full stack
echo.
pause
