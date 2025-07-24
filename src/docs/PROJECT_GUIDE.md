# PDF API Project - Setup and Usage Guide

## Overview
This project creates a comprehensive PDF management API with AI-powered querying capabilities. It allows users to upload PDF documents, extract text content, and query the content using Large Language Models (LLMs).

## File Structure and Purpose

### Core Application Files
- **`app.py`** - Main Flask application entry point
- **`config.py`** - Configuration settings and environment variables
- **`requirements.txt`** - Python dependencies
- **`.env`** - Environment variables (API keys, secrets)

### Models (Database Layer)
- **`models/__init__.py`** - Models package initialization
- **`models/document.py`** - Document model for database operations

### Routes (API Endpoints)
- **`routes/__init__.py`** - Routes package initialization
- **`routes/upload.py`** - PDF upload endpoints
- **`routes/query.py`** - AI querying endpoints
- **`routes/crud.py`** - CRUD operations for documents

### Services (Business Logic)
- **`services/__init__.py`** - Services package initialization
- **`services/pdf_service.py`** - PDF processing and text extraction
- **`services/llm_service.py`** - LLM integration (OpenAI API)

### Frontend
- **`templates/`** - HTML templates
  - `index.html` - Home page
  - `upload.html` - Upload page
  - `query.html` - Query page
- **`static/css/style.css`** - Styling
- **`static/js/main.js`** - Frontend JavaScript

### Storage
- **`uploads/`** - Directory for uploaded PDF files

## How Files Connect

### 1. Application Flow
```
app.py (main) 
  ├── Imports models (document.py)
  ├── Imports routes (upload.py, query.py, crud.py)
  └── Serves HTML templates
```

### 2. Request Flow
```
User Request → Routes → Services → Models → Database
                 ↓
              Templates ← Static Files
```

### 3. Dependencies
```
Routes depend on:
  - Models (for database operations)
  - Services (for business logic)
  - Flask utilities

Services depend on:
  - External libraries (PyPDF2, OpenAI)
  - Configuration settings
```

## API Endpoints Reference

### Upload Operations
- `POST /api/upload` - Upload PDF file
- `GET /api/upload/status/<id>` - Check upload status

### Query Operations
- `POST /api/query` - Query documents with AI
- `GET /api/query/suggestions` - Get suggested queries
- `GET /api/documents/<id>/summary` - Get AI summary

### CRUD Operations
- `GET /api/documents` - List all documents (with pagination)
- `GET /api/documents/<id>` - Get specific document
- `PUT /api/documents/<id>` - Update document metadata
- `DELETE /api/documents/<id>` - Delete document
- `GET /api/documents/search` - Search documents
- `GET /api/documents/stats` - Get statistics

## Configuration Guide

### Environment Variables
Create a `.env` file with these variables:
```
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///pdf_api.db
```

### Getting OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste into your `.env` file

## Database Schema

### Document Table
- `id` - Primary key
- `filename` - Stored filename
- `original_filename` - Original uploaded filename
- `file_path` - Full path to stored file
- `content` - Extracted text content
- `file_size` - File size in bytes
- `upload_date` - Upload timestamp
- `description` - User-provided description
- `tags` - Comma-separated tags

## Error Handling

### Common Issues and Solutions

1. **Import Errors** - Install dependencies with `pip install -r requirements.txt`
2. **Database Errors** - Initialize database with provided commands
3. **File Upload Errors** - Check file permissions and upload directory
4. **API Errors** - Verify OpenAI API key is valid and has credits

## Security Considerations

1. **File Validation** - Only PDF files are accepted
2. **File Size Limits** - Maximum 16MB per file
3. **Secure Filenames** - Filenames are sanitized
4. **API Key Protection** - API keys stored in environment variables
5. **Input Validation** - All inputs are validated and sanitized

## Performance Optimization

1. **Database Indexing** - Consider adding indexes for search operations
2. **File Storage** - Large files stored on disk, not in database
3. **Pagination** - Large document lists are paginated
4. **Content Limits** - Text content is limited to prevent token overflow

## Extending the Application

### Adding New Features
1. **New Routes** - Add to `routes/` directory
2. **New Models** - Add to `models/` directory
3. **New Services** - Add to `services/` directory
4. **New Frontend** - Add templates and update static files

### Integration Options
1. **Different LLM Providers** - Modify `llm_service.py`
2. **Cloud Storage** - Update `pdf_service.py` for cloud uploads
3. **Authentication** - Add user management system
4. **Real-time Updates** - Add WebSocket support

This structure ensures maintainability, scalability, and clear separation of concerns.
