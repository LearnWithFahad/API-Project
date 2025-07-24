from dotenv import load_dotenv
load_dotenv()  # Load environment variables before anything else

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
import os

# Initialize Flask extensions
db = SQLAlchemy()

def create_app(config_name=None):
    """Application factory with security enhancements"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize configuration
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS securely
    CORS(app, 
         origins=os.environ.get('ALLOWED_ORIGINS', 'http://localhost:*').split(','),
         methods=['GET', 'POST', 'PUT', 'DELETE'],
         allow_headers=['Content-Type', 'Authorization', 'X-API-Key']
    )
    
    # Initialize security middleware
    try:
        from security.middleware import SecurityMiddleware
        SecurityMiddleware(app)
    except ImportError:
        print("Warning: Security middleware not available")
    
    # Register blueprints
    try:
        from routes.upload_simple import upload_bp
        from routes.query_simple import query_bp  
        # from routes.crud_simple import crud_bp  # Temporarily commented out
        
        app.register_blueprint(upload_bp, url_prefix='/api')
        app.register_blueprint(query_bp, url_prefix='/api')
        # app.register_blueprint(crud_bp, url_prefix='/api')  # Temporarily commented out
    except ImportError as e:
        print(f"Warning: Some routes not available: {e}")
    
    # Initialize database
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    
    # Main routes for HTML pages
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload')
    def upload_page():
        return render_template('upload.html')

    @app.route('/query')
    def query_page():
        return render_template('query.html')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Simple health check endpoint"""
        return jsonify({'status': 'healthy', 'message': 'Server is running'}), 200
    
    # Documents endpoint with pure SQLite
    @app.route('/api/documents', methods=['GET'])
    def api_documents():
        """Direct documents endpoint using SQLite"""
        try:
            documents_data = []
            
            # Get pagination parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            # Direct SQLite query
            import sqlite3
            import os
            
            db_path = os.path.join(os.path.dirname(__file__), 'instance', 'pdf_api.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM document")
            total_result = cursor.fetchone()
            total = total_result[0] if total_result else 0
            
            # Get documents with pagination
            offset = (page - 1) * per_page
            cursor.execute("""
                SELECT id, filename, original_filename, file_path, content, 
                       file_size, upload_date, description, tags 
                FROM document 
                ORDER BY upload_date DESC 
                LIMIT ? OFFSET ?
            """, (per_page, offset))
            
            rows = cursor.fetchall()
            
            for row in rows:
                doc_data = {
                    'id': row[0],
                    'filename': row[1],
                    'original_filename': row[2],
                    'file_path': row[3],
                    'content': row[4][:200] + '...' if row[4] and len(row[4]) > 200 else row[4],  # Truncate content for display
                    'file_size': row[5],
                    'upload_date': row[6],
                    'description': row[7],
                    'tags': row[8].split(',') if row[8] else []
                }
                documents_data.append(doc_data)
            
            conn.close()
            
            pages = (total + per_page - 1) // per_page if total > 0 else 1
            
            return jsonify({
                'documents': documents_data,
                'total': total,
                'page': page,
                'pages': pages,
                'per_page': per_page
            }), 200
            
        except Exception as e:
            print(f"Error in documents endpoint: {str(e)}")
            return jsonify({'error': f'Database query failed: {str(e)}'}), 500
    
    # Documents stats endpoint
    @app.route('/api/documents/stats', methods=['GET'])
    def api_documents_stats():
        """Get document statistics"""
        try:
            import sqlite3
            import os
            
            db_path = os.path.join(os.path.dirname(__file__), 'instance', 'pdf_api.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get total document count
            cursor.execute("SELECT COUNT(*) FROM document")
            total_documents = cursor.fetchone()[0]
            
            # Get total file size
            cursor.execute("SELECT SUM(file_size) FROM document")
            total_size_result = cursor.fetchone()
            total_size = total_size_result[0] if total_size_result[0] else 0
            
            conn.close()
            
            return jsonify({
                'total_documents': total_documents,
                'total_size': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2) if total_size else 0
            }), 200
            
        except Exception as e:
            print(f"Error in documents stats endpoint: {str(e)}")
            return jsonify({'error': f'Stats query failed: {str(e)}'}), 500
    
    # Delete document endpoint
    @app.route('/api/documents/<int:document_id>', methods=['DELETE'])
    def delete_document(document_id):
        """Delete a document and its file"""
        try:
            import sqlite3
            import os
            
            db_path = os.path.join(os.path.dirname(__file__), 'instance', 'pdf_api.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # First, get the document to find the file path
            cursor.execute("SELECT file_path FROM document WHERE id = ?", (document_id,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return jsonify({'error': 'Document not found'}), 404
            
            file_path = result[0]
            
            # Delete the physical file
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except OSError as e:
                    print(f"Warning: Could not delete file {file_path}: {e}")
            
            # Delete from database
            cursor.execute("DELETE FROM document WHERE id = ?", (document_id,))
            
            if cursor.rowcount == 0:
                conn.close()
                return jsonify({'error': 'Document not found'}), 404
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'message': 'Document deleted successfully',
                'document_id': document_id
            }), 200
            
        except Exception as e:
            print(f"Error deleting document: {str(e)}")
            return jsonify({'error': f'Failed to delete document: {str(e)}'}), 500
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'error': 'File too large'}), 413
    
    @app.errorhandler(429)
    def ratelimit_handler(error):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        try:
            from security.middleware import log_security_event, get_client_ip
            log_security_event("INTERNAL_ERROR", str(error), get_client_ip())
        except ImportError:
            print(f"Internal error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Production vs Development
    if os.environ.get('FLASK_ENV') == 'production':
        # Production settings
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
    else:
        # Development settings
        app.run(debug=True, host='127.0.0.1', port=5000)
