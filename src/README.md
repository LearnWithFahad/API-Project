# 📄 PDF API Project

A professional Flask-based PDF management API with AI querying capabilities using Google Gemini.

## 🎯 What This Project Does

This application allows you to:
- **Upload PDF files** through a web interface
- **Extract text** from PDF documents automatically
- **Query documents** using AI (Google Gemini) in natural language
- **Manage documents** with full CRUD operations
- **View document statistics** and history

## 🏗️ Project Structure

```
PDF_API_Project/
├── 📁 src/                          # Source code
│   ├── 📄 app.py                    # Main application (SQLAlchemy version)
│   ├── 📄 app_simple.py             # Simple application (SQLite version) ⭐ CURRENT
│   ├── 📄 config.py                 # Configuration settings
│   │
│   ├── 📁 models/                   # Database models
│   │   ├── 📄 __init__.py
│   │   └── 📄 document.py           # Document data model
│   │
│   ├── 📁 routes/                   # API endpoints
│   │   ├── 📄 __init__.py
│   │   ├── 📄 upload_simple.py      # File upload endpoints ⭐
│   │   ├── 📄 query_simple.py       # AI query endpoints ⭐
│   │   ├── 📄 crud_simple.py        # Document CRUD endpoints ⭐
│   │   ├── 📄 upload.py             # SQLAlchemy version
│   │   ├── 📄 query.py              # SQLAlchemy version
│   │   └── 📄 crud.py               # SQLAlchemy version
│   │
│   ├── 📁 services/                 # Business logic
│   │   ├── 📄 __init__.py
│   │   ├── 📄 llm_service.py        # Google Gemini AI integration ⭐
│   │   └── 📄 pdf_service.py        # PDF text extraction ⭐
│   │
│   ├── 📁 static/                   # CSS, JavaScript, images
│   │   ├── 📁 css/
│   │   │   └── 📄 style.css         # Main stylesheet
│   │   └── 📁 js/
│   │       └── 📄 main.js           # Frontend JavaScript
│   │
│   ├── 📁 templates/                # HTML templates
│   │   ├── 📄 index.html            # Home page
│   │   ├── 📄 upload.html           # Upload interface
│   │   └── 📄 query.html            # Query interface
│   │
│   ├── 📁 security/                 # Security middleware
│   │   ├── 📄 file_validator.py     # File validation
│   │   ├── 📄 input_validator.py    # Input sanitization
│   │   └── 📄 middleware.py         # Security middleware
│   │
│   ├── 📁 uploads/                  # Uploaded PDF files
│   └── 📁 instance/                 # Database files
│       └── 📄 pdf_api.db            # SQLite database
│
├── 📁 docs/                         # Documentation (move here)
│   ├── 📄 BEGINNER_GUIDE.md         # Step-by-step guide for beginners
│   ├── 📄 PROJECT_GUIDE.md          # Detailed project documentation
│   ├── 📄 SECURITY.md               # Security considerations
│   └── 📄 SETUP_COMMANDS.md         # Setup instructions
│
├── 📁 tests/                        # Test files (move here)
│   ├── 📄 test_upload.py            # Upload functionality tests
│   ├── 📄 test_llm.py               # AI service tests
│   └── 📄 security_test.py          # Security tests
│
├── 📁 scripts/                      # Utility scripts (move here)
│   ├── 📄 setup_security.py         # Security setup
│   └── 📄 restart.py                # Server restart utility
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 requirements-security.txt     # Security-focused dependencies
├── 📄 .env.example                  # Environment variables template
└── 📄 README.md                     # This file
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd PDF_API_Project

# Create virtual environment
python -m venv pdf_api_env

# Activate virtual environment
# On Windows:
pdf_api_env\\Scripts\\activate
# On macOS/Linux:
source pdf_api_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Google Gemini API key
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application

```bash
# Navigate to source directory
cd src

# Run the simple version (recommended for beginners)
python app_simple.py

# Alternative: Use startup scripts
# Windows:
start.bat

# macOS/Linux:
./start.sh
```

### 5. Access the Application

- **Home Page**: http://localhost:5000
- **Upload PDFs**: http://localhost:5000/upload
- **Query Documents**: http://localhost:5000/query
- **API Health Check**: http://localhost:5000/api/health

## 🔧 How It Works

### 1. **File Upload Flow**
```
User uploads PDF → File validation → Text extraction → Save to database → Store file
```

### 2. **AI Query Flow**
```
User asks question → Select document(s) → Send to Gemini AI → Process response → Display answer
```

### 3. **Document Management Flow**
```
View documents → Select actions (Query/Delete) → Perform operation → Update interface
```

## 🎯 Key Features

### ✅ **Core Functionality**
- PDF file upload with validation
- Automatic text extraction from PDFs
- AI-powered document querying
- Full CRUD operations for documents
- Query history management
- Document statistics

### 🔒 **Security Features**
- File type validation (PDF only)
- File size limits (16MB max)
- Input sanitization
- Secure filename handling
- API rate limiting considerations

### 🎨 **User Interface**
- Clean, responsive web interface
- Real-time feedback
- Query suggestions
- Document management dashboard
- Mobile-friendly design

## 🛠️ API Endpoints

### Document Upload
- `POST /api/upload` - Upload a PDF file

### Document Query
- `POST /api/query` - Query documents with AI
- `GET /api/query/suggestions` - Get query suggestions

### Document Management
- `GET /api/documents` - List all documents
- `GET /api/documents/<id>` - Get specific document
- `DELETE /api/documents/<id>` - Delete document
- `GET /api/stats` - Get document statistics

### Health Check
- `GET /api/health` - API health status

## 🤖 AI Integration

This project uses **Google Gemini AI** for document querying:

- **Model**: gemini-1.5-flash-latest
- **Capabilities**: Text analysis, question answering, summarization
- **Features**: Context-aware responses, multi-document queries

## 📚 For Beginners

### Understanding the Code Flow

1. **Entry Point**: `app_simple.py` - This is where the application starts
2. **Routes**: Files in `routes/` folder - These handle web requests
3. **Services**: Files in `services/` folder - These contain business logic
4. **Templates**: Files in `templates/` folder - These are the web pages
5. **Static Files**: Files in `static/` folder - CSS and JavaScript

### Key Files to Understand

1. **`app_simple.py`** - Main application file
2. **`routes/upload_simple.py`** - Handles file uploads
3. **`routes/query_simple.py`** - Handles AI queries
4. **`services/llm_service.py`** - Connects to Google Gemini
5. **`services/pdf_service.py`** - Extracts text from PDFs

## 🔧 Development

### Running Tests
```bash
python test_upload.py
python test_llm.py
```

### Adding New Features
1. Add new routes in `routes/` folder
2. Add business logic in `services/` folder
3. Update templates if needed
4. Add tests for new functionality

## 📈 Production Deployment

For production deployment, consider:
- Use a production WSGI server (Gunicorn, uWSGI)
- Set up proper environment variables
- Configure database backups
- Implement proper logging
- Set up monitoring and health checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the documentation in the `docs/` folder
2. Look at existing issues in the repository
3. Create a new issue with detailed information

## 🎉 Acknowledgments

- Flask framework for web development
- Google Gemini for AI capabilities
- PyPDF2 for PDF text extraction
- SQLite for database storage

---

**Happy coding! 🚀**
