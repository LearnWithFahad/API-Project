# Essential Files for PDF API Program Execution

## Core Application Files (Required)
```
├── app_simple.py              # Main Flask application
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys)
├── .env.example              # Environment template
├── start.bat                  # Windows startup script
├── start.sh                   # Linux/Mac startup script
└── .gitignore                # Git ignore rules
```

## Application Structure (Required)
```
├── models/
│   ├── __init__.py
│   └── document.py           # Database model
├── routes/
│   ├── __init__.py
│   ├── upload_simple.py      # File upload endpoints
│   ├── query_simple.py       # AI query endpoints
│   └── crud_simple.py        # CRUD operations
├── services/
│   ├── __init__.py
│   ├── pdf_service.py        # PDF processing
│   └── llm_service.py        # Gemini API integration
├── security/
│   ├── __init__.py
│   ├── file_validator.py     # File validation
│   ├── input_validator.py    # Input sanitization
│   └── middleware.py         # Security middleware
├── templates/
│   ├── index.html            # Main page
│   ├── upload.html           # Upload interface
│   └── query.html            # Query interface
├── static/
│   ├── css/
│   │   └── style.css         # Styling
│   └── js/
│       └── main.js           # Frontend JavaScript
├── uploads/                  # PDF file storage (created automatically)
└── instance/                 # Database storage (created automatically)
    └── pdf_api.db            # SQLite database
```

## Documentation (Optional but Recommended)
```
├── README.md                 # Main project documentation
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # License file
├── QUICK_START.md           # Quick start guide
├── RUN_COMMANDS.md          # Server commands
├── SECURITY_ASSESSMENT.md   # Security analysis
├── docs/                    # Additional documentation
├── tests/                   # Test files (optional)
└── scripts/                 # Utility scripts (optional)
```

## Development Environment
```
├── pdf_api_env/             # Virtual environment
├── .vscode/                 # VS Code settings (optional)
└── .github/                 # GitHub configuration (optional)
```

## Files Removed (Were Not Used)
- ❌ app.py (duplicate of app_simple.py)
- ❌ routes/crud.py, routes/upload.py, routes/query.py (non-simple versions)
- ❌ convert_guide_to_pdf.py, enhanced_pdf_converter.py, simple_pdf_converter.py
- ❌ convert_to_pdf.bat
- ❌ README_NEW.md, CLEANUP_SUMMARY.md, PROJECT_SUMMARY.md (duplicates)
- ❌ test_endpoint.py (standalone test)
- ❌ scripts/create_diagram.py, scripts/restart.py (utilities)
- ❌ __pycache__/ directories (Python cache)
- ❌ *.pyc files (compiled Python)

## Current Program Flow
The cleaned project now has a clear execution path:
1. **Entry Point**: `app_simple.py`
2. **Routes**: `routes/*_simple.py` files
3. **Services**: `services/pdf_service.py` and `services/llm_service.py`
4. **Security**: `security/` folder for validation and middleware
5. **Frontend**: `templates/` and `static/` for user interface
6. **Storage**: `uploads/` for files, `instance/` for database

The project is now streamlined with only essential files needed for execution.
