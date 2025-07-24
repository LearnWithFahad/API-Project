# ⚡ Quick Start - PDF API Server

## 🚀 Essential Commands (Copy & Paste)

### 1. Setup (First Time Only)
```bash
# Create virtual environment
python -m venv pdf_api_env

# Activate virtual environment
# Windows:
pdf_api_env\Scripts\activate
# Mac/Linux:
source pdf_api_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Start Server
```bash
# Method 1: Simple (Recommended)
python app_simple.py

# Method 2: Use startup script
# Windows:
start.bat
# Mac/Linux:
./start.sh
```

### 3. Access Application
- **Web Interface**: http://localhost:5000
- **Upload PDFs**: http://localhost:5000/upload
- **Query Docs**: http://localhost:5000/query
- **API Health**: http://localhost:5000/api/health

### 4. Stop Server
```bash
# Press in terminal where server is running:
Ctrl + C
```

### 5. Test Commands
```bash
# Test API health
curl http://localhost:5000/api/health

# Test upload (replace path)
curl -X POST -F "file=@your-document.pdf" http://localhost:5000/api/upload

# Test query
curl -X POST http://localhost:5000/api/query -H "Content-Type: application/json" -d '{"query": "What is this about?"}'
```

---

## 🔧 Troubleshooting

**Server won't start?**
```bash
# Check Python version
python --version

# Check if virtual environment is active
which python  # Mac/Linux
where python   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Need Gemini API Key?**
1. Go to: https://makersuite.google.com/app/apikey
2. Create API key
3. Add to `.env` file: `GEMINI_API_KEY=your_key_here`

**Port already in use?**
```bash
# Kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti :5000 | xargs kill -9
```

---

**🎯 Most Common Workflow:**
1. `pdf_api_env\Scripts\activate` (Windows) or `source pdf_api_env/bin/activate` (Mac/Linux)
2. `python app_simple.py`  
3. Open http://localhost:5000
4. Upload PDFs and start querying! 🚀
