from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import time

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload PDF file endpoint"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        original_filename = file.filename
        
        # Create unique filename to avoid conflicts
        timestamp = str(int(time.time() * 1000))
        unique_filename = f"{timestamp}_{filename}"
        
        # Save file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Extract text content from PDF
        try:
            from services.pdf_service import PDFService
            pdf_service = PDFService()
            content = pdf_service.extract_text(file_path)
        except ImportError:
            content = "PDF content extraction not available"
        except Exception as e:
            content = f"Failed to extract content: {str(e)}"
        
        # Get additional data from form
        description = request.form.get('description', '')
        tags = request.form.get('tags', '')
        
        # Auto-generate summary and keywords using AI if content is available
        auto_summary = ""
        auto_keywords = ""
        
        if content and len(content.strip()) > 50:  # Only if we have meaningful content
            try:
                from services.llm_service import LLMService
                llm_service = LLMService()
                
                if llm_service.is_available():
                    # Generate summary
                    summary_result = llm_service.generate_summary(content, max_tokens=200)
                    if summary_result and "Error" not in summary_result:
                        auto_summary = summary_result
                    
                    # Extract keywords
                    keywords_list = llm_service.extract_keywords(content, max_tokens=50)
                    if keywords_list and len(keywords_list) > 0:
                        auto_keywords = ", ".join(keywords_list[:10])  # Limit to 10 keywords
                        
            except Exception as e:
                print(f"AI processing failed: {e}")
                # Continue without AI features
                pass
        
        # Combine user tags with auto-generated keywords
        final_tags = tags
        if auto_keywords:
            if final_tags:
                final_tags += f", {auto_keywords}"
            else:
                final_tags = auto_keywords
        
        # Use auto-generated summary if no description provided
        final_description = description
        if not final_description and auto_summary:
            final_description = auto_summary
        
        # Create document record using SQLite
        import sqlite3
        from datetime import datetime
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'pdf_api.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insert document into database
        cursor.execute("""
            INSERT INTO document (filename, original_filename, file_path, content, 
                                file_size, upload_date, description, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (unique_filename, original_filename, file_path, content, 
              file_size, datetime.now().isoformat(), final_description, final_tags))
        
        document_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'File uploaded successfully',
            'document': {
                'id': document_id,
                'filename': unique_filename,
                'original_filename': original_filename,
                'file_path': file_path,
                'file_size': file_size,
                'description': final_description,
                'tags': final_tags.split(',') if final_tags else []
            },
            'ai_features': {
                'auto_summary_generated': bool(auto_summary),
                'auto_keywords_generated': bool(auto_keywords)
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/upload/status/<int:document_id>', methods=['GET'])
def get_upload_status(document_id):
    """Get upload status for a document"""
    try:
        import sqlite3
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'pdf_api.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, filename, original_filename, file_path, content, 
                   file_size, upload_date, description, tags 
            FROM document WHERE id = ?
        """, (document_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Document not found'}), 404
        
        document_data = {
            'id': row[0],
            'filename': row[1],
            'original_filename': row[2],
            'file_path': row[3],
            'content': row[4],
            'file_size': row[5],
            'upload_date': row[6],
            'description': row[7],
            'tags': row[8].split(',') if row[8] else []
        }
        return jsonify({
            'status': 'completed',
            'document': document_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
