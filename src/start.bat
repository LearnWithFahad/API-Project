@echo off
REM PDF API Project - Windows Startup Script

echo 🚀 Starting PDF API Project...

REM Check if virtual environment exists
if not exist "pdf_api_env" (
    echo ❌ Virtual environment not found. Please run setup first:
    echo    python -m venv pdf_api_env
    echo    pdf_api_env\Scripts\activate
    echo    pip install -r requirements.txt
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ❌ Environment file not found. Please:
    echo    1. Copy .env.example to .env
    echo    2. Add your GEMINI_API_KEY
    exit /b 1
)

echo ✅ Environment checks passed
echo 📄 Starting server on http://localhost:5000
echo 💡 Press Ctrl+C to stop the server

REM Start the application
python app_simple.py
