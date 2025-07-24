# PDF API Project - Complete Setup Commands

## Prerequisites
- Python 3.8 or higher installed
- Git installed (optional)
- A text editor or IDE (VS Code recommended)

## Step-by-Step Setup Commands

Run these commands one by one in your terminal:

### 1. Navigate to the project directory
```bash
cd "c:\Users\IT GENICS\Documents\API_Project\src"
```

### 2. Create a virtual environment
```bash
python -m venv pdf_api_env
```

### 3. Activate the virtual environment (Windows)
```bash
pdf_api_env\Scripts\activate
```

### 4. Upgrade pip
```bash
python -m pip install --upgrade pip
```

### 5. Install required packages
```bash
pip install -r requirements.txt
```

### 6. Set up environment variables
Create a .env file with your settings:
```bash
echo OPENAI_API_KEY=your_api_key_here > .env
echo FLASK_ENV=development >> .env
echo SECRET_KEY=your_secret_key_here >> .env
```

### 7. Initialize the database
```bash
python -c "from app_simple import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### 8. Test the installation
```bash
python app_simple.py
```

### 9. Open your browser
Navigate to: http://localhost:5000

## Alternative Commands for Different Environments

### For macOS/Linux users:
Replace step 3 with:
```bash
source pdf_api_env/bin/activate
```

### For PowerShell users:
Replace step 3 with:
```bash
pdf_api_env\Scripts\Activate.ps1
```

## Verification Steps

After running the setup, verify everything is working:

1. **Check if Flask is running**: You should see output like:
   ```
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
   * Running on http://[your-ip]:5000
   ```

2. **Test the web interface**: 
   - Go to http://localhost:5000
   - You should see the PDF API homepage

3. **Test file upload**:
   - Go to http://localhost:5000/upload
   - Try uploading a sample PDF

## Troubleshooting Common Issues

### Issue: "python: command not found"
**Solution**: Try using `python3` instead of `python`

### Issue: "pip: command not found"
**Solution**: Try using `python -m pip` instead of `pip`

### Issue: "Permission denied"
**Solution**: On Windows, run Command Prompt as Administrator

### Issue: "Module not found"
**Solution**: Make sure virtual environment is activated

### Issue: "Port already in use"
**Solution**: Kill any existing Python processes or change the port in app_simple.py

## Getting an OpenAI API Key

1. Visit: https://platform.openai.com/
2. Sign up or log in to your account
3. Go to API Keys section
4. Create a new API key
5. Copy the key and paste it in your .env file

## Project Structure Explanation

- `app_simple.py` - Main Flask application (simplified version)
- `config.py` - Configuration settings
- `models/` - Database models
- `routes/` - API endpoints
- `services/` - Business logic
- `templates/` - HTML files
- `static/` - CSS and JavaScript
- `uploads/` - PDF storage directory

## Next Steps

Once the application is running:

1. **Upload PDFs**: Use the upload page to add PDF documents
2. **Query content**: Use the query page to ask questions about your documents
3. **Manage documents**: View, update, and delete documents through the interface

## Development Tips

- Always activate the virtual environment before working
- Check the terminal for error messages
- Use the browser's developer tools to debug frontend issues
- Restart the Flask app after making code changes

## Production Deployment

For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Using a production database (PostgreSQL, MySQL)
- Implementing proper logging and monitoring
