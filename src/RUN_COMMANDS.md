# 🚀 PDF API Server - Quick Start Commands

## Prerequisites
- Python 3.8+ installed
- Git (optional, for cloning)

## 1. Setup Commands

### Clone/Navigate to Project
```bash
# If cloning from GitHub
git clone <your-repo-url>
cd PDF_API_Project/src

# Or if you already have the project
cd path/to/PDF_API_Project/src
```

### Create Virtual Environment
```bash
# Windows
python -m venv pdf_api_env
pdf_api_env\Scripts\activate

# macOS/Linux
python3 -m venv pdf_api_env
source pdf_api_env/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Configuration

### Set up Environment Variables
```bash
# Copy the template
cp .env.example .env

# Edit .env file and add your Gemini API key
# Windows (using notepad)
notepad .env

# macOS/Linux (using nano)
nano .env
```

**Add this to your .env file:**
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
```

## 3. Run the Server

### Method 1: Using Startup Scripts (Recommended)
```bash
# Windows
start.bat

# macOS/Linux
./start.sh
```

### Method 2: Direct Python Command
```bash
python app_simple.py
```

### Method 3: Using Flask Command
```bash
# Set Flask app
export FLASK_APP=app_simple.py  # macOS/Linux
set FLASK_APP=app_simple.py     # Windows

# Run with Flask
flask run --host=0.0.0.0 --port=5000 --debug
```

## 4. Access the Application

Once the server starts, access these URLs:

### Web Interface
- **Home Page**: http://localhost:5000
- **Upload PDFs**: http://localhost:5000/upload  
- **Query Documents**: http://localhost:5000/query

### API Endpoints
- **Health Check**: http://localhost:5000/api/health
- **Upload API**: POST http://localhost:5000/api/upload
- **Query API**: POST http://localhost:5000/api/query
- **Documents API**: GET http://localhost:5000/api/documents

## 5. Testing Commands

### Run Tests
```bash
# Run all tests
python tests/test_upload.py
python tests/test_llm.py
python tests/test_endpoint.py

# Run security tests
python tests/security_test.py
```

### Test API Endpoints with curl
```bash
# Health check
curl http://localhost:5000/api/health

# Get all documents
curl http://localhost:5000/api/documents

# Upload a PDF (replace with actual file path)
curl -X POST -F "file=@path/to/your/document.pdf" http://localhost:5000/api/upload

# Query documents
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?"}'
```

## 6. Development Commands

### Install Additional Dependencies
```bash
# Security dependencies
pip install -r requirements-security.txt

# Development dependencies
pip install pytest flask-testing
```

### Database Management
```bash
# View database location
ls -la instance/

# Check database contents (requires sqlite3)
sqlite3 instance/pdf_api.db ".tables"
sqlite3 instance/pdf_api.db "SELECT * FROM document;"
```

### Restart Server
```bash
# Using restart script
python scripts/restart.py

# Or manually stop (Ctrl+C) and restart
python app_simple.py
```

## 7. Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### Check Installed Packages
```bash
pip list
```

### Check Virtual Environment
```bash
# Windows
where python

# macOS/Linux  
which python
```

### View Server Logs
```bash
# Server logs are displayed in terminal
# For file logging, check app.log (if configured)
tail -f app.log
```

### Clear Cache and Temp Files
```bash
# Remove Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +

# Clear uploaded files (be careful!)
rm -rf uploads/*

# Reset database (be careful!)
rm -f instance/pdf_api.db
```

## 8. Production Deployment Commands

### Install Production WSGI Server
```bash
pip install gunicorn
```

### Run with Gunicorn (Production)
```bash
# Basic production run
gunicorn -w 4 -b 0.0.0.0:5000 app_simple:app

# With logging
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - app_simple:app
```

### Environment Variables for Production
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export GEMINI_API_KEY=your_production_api_key
```

## 9. Docker Commands (Optional)

### Create Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app_simple.py"]
```

### Docker Commands
```bash
# Build image
docker build -t pdf-api .

# Run container
docker run -p 5000:5000 -e GEMINI_API_KEY=your_key pdf-api
```

## 10. Stop the Server

### Stop Development Server
```bash
# In terminal where server is running
Ctrl + C
```

### Stop Background Processes
```bash
# Find Python processes
ps aux | grep python

# Kill specific process (replace PID)
kill <PID>

# Kill all Python processes (be careful!)
pkill -f python
```

---

## 🎯 Quick Start Summary

**Minimum commands to get started:**

1. `cd PDF_API_Project/src`
2. `python -m venv pdf_api_env`
3. `pdf_api_env\Scripts\activate` (Windows) or `source pdf_api_env/bin/activate` (Mac/Linux)
4. `pip install -r requirements.txt`
5. `cp .env.example .env` (then edit .env with your Gemini API key)
6. `python app_simple.py`
7. Open http://localhost:5000

**That's it! Your PDF API server is running! 🚀**
