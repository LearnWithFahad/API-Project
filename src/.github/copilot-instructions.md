<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# PDF API Project - Copilot Instructions

This is a Flask-based PDF management API with AI querying capabilities.

## Project Context
- **Language**: Python 3.8+
- **Framework**: Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: OpenAI API
- **PDF Processing**: PyPDF2

## Architecture Patterns
- **MVC Pattern**: Models, Routes (Controllers), Templates (Views)
- **Service Layer**: Business logic separated into services
- **Blueprint Pattern**: Routes organized as Flask blueprints

## Code Style Guidelines
- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Include error handling in all API endpoints
- Add docstrings to all functions and classes
- Use type hints where appropriate

## Key Dependencies
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- PyPDF2: PDF text extraction
- OpenAI: LLM integration
- Flask-CORS: Cross-origin requests

## Security Considerations
- Validate all file uploads (PDF only)
- Sanitize filenames using werkzeug.utils.secure_filename
- Limit file sizes (16MB max)
- Use environment variables for API keys
- Validate and sanitize all user inputs

## Common Patterns
- Use Blueprint for route organization
- Return JSON responses from API endpoints
- Include proper HTTP status codes
- Handle exceptions gracefully
- Use consistent error response format

## File Structure
- `models/`: Database models
- `routes/`: API endpoints (blueprints)
- `services/`: Business logic
- `templates/`: HTML templates
- `static/`: CSS and JavaScript files
- `uploads/`: PDF file storage

When generating code, ensure it follows these patterns and integrates well with the existing codebase.
