#!/bin/bash
# Script to run both FastAPI backend and Streamlit UI
# Usage: bash run_full_stack.sh

echo "=========================================="
echo "Document Extraction Platform - Full Stack"
echo "=========================================="
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found!"
    exit 1
fi

echo ""
echo "Starting FastAPI Backend..."
echo "=========================================="
# Start backend in background
uvicorn app.main:app --reload --log-level info &
BACKEND_PID=$!

sleep 3

echo ""
echo "Starting Streamlit UI..."
echo "=========================================="
# Start Streamlit
streamlit run streamlit_ui/app.py

# On exit, kill background backend
trap "kill $BACKEND_PID" EXIT
