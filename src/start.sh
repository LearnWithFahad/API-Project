#!/bin/bash
# PDF API Project - Startup Script

echo "🚀 Starting PDF API Project..."

# Check if virtual environment exists
if [ ! -d "pdf_api_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python -m venv pdf_api_env"
    echo "   pdf_api_env\\Scripts\\activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Environment file not found. Please:"
    echo "   1. Copy .env.example to .env"
    echo "   2. Add your GEMINI_API_KEY"
    exit 1
fi

echo "✅ Environment checks passed"
echo "📄 Starting server on http://localhost:5000"
echo "💡 Press Ctrl+C to stop the server"

# Start the application
python app_simple.py
