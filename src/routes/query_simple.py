from flask import Blueprint, request, jsonify
from services.llm_service import LLMService

query_bp = Blueprint('query', __name__)

@query_bp.route('/query', methods=['POST'])
def query_documents():
    """Query documents with AI"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        document_id = data.get('document_id')  # Get specific document ID if provided
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if len(query.strip()) < 3:
            return jsonify({'error': 'Query must be at least 3 characters long'}), 400
        
        # Get documents from database using SQLite
        import sqlite3
        import os
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'pdf_api.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query specific document or all documents
        if document_id:
            cursor.execute("""
                SELECT id, filename, content, description 
                FROM document 
                WHERE id = ? AND content IS NOT NULL AND content != ''
            """, (document_id,))
        else:
            cursor.execute("""
                SELECT id, filename, content, description 
                FROM document 
                WHERE content IS NOT NULL AND content != ''
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            if document_id:
                return jsonify({
                    'error': f'Document with ID {document_id} not found or has no content',
                    'query': query,
                    'results': [],
                    'answer': f'Document with ID {document_id} was not found. Please check if the document exists and has readable content.'
                }), 404
            else:
                return jsonify({
                    'message': 'No documents found',
                    'query': query,
                    'results': [],
                    'answer': 'No documents have been uploaded yet. Please upload some PDF files first.'
                }), 200
        
        # Extract content from documents
        documents_content = []
        document_info = []
        
        for row in rows:
            doc_id, filename, content, description = row
            if content and content.strip():
                documents_content.append(content)
                document_info.append({
                    'id': doc_id,
                    'filename': filename,
                    'description': description
                })
        
        if not documents_content:
            return jsonify({
                'message': 'No document content available',
                'query': query,
                'results': [],
                'answer': 'The uploaded documents do not contain readable text content.'
            }), 200
        
        # Initialize LLM service and query documents
        llm_service = LLMService()
        
        if not llm_service.is_available():
            return jsonify({
                'error': 'AI service is not available. Please check Gemini API key configuration.',
                'query': query,
                'results': [],
                'answer': None
            }), 500
        
        # Query the documents using AI with Gemini
        # Combine document content for context
        if len(documents_content) == 1:
            # Single document query
            combined_context = documents_content[0]
            context_info = f"Analyzing document: {document_info[0]['filename']}"
        else:
            # Multiple documents query
            combined_context = "\n\n".join(documents_content)
            context_info = f"Analyzing {len(documents_content)} documents"
            
        answer = llm_service.query_content(query, combined_context)
        
        if answer and not answer.startswith("Error"):
            return jsonify({
                'message': 'Query processed successfully',
                'query': query,
                'answer': answer,
                'model_used': 'Gemini Pro',
                'tokens_used': 0,  # Gemini doesn't return token count
                'documents_searched': len(documents_content),
                'document_info': document_info,
                'context_info': context_info,
                'document_id_queried': document_id if document_id else None,
                'success': True
            }), 200
        else:
            return jsonify({
                'error': answer if answer else 'Unknown error occurred',
                'query': query,
                'answer': None,
                'success': False
            }), 500
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'query': query if 'query' in locals() else '',
            'answer': None,
            'success': False
        }), 500

@query_bp.route('/documents', methods=['GET'])
def get_documents():
    """Get all documents"""
    try:
        import sqlite3
        import os
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'pdf_api.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, filename, original_filename, file_path, content, 
                   file_size, upload_date, description, tags 
            FROM document 
            ORDER BY upload_date DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        documents = []
        for row in rows:
            doc_data = {
                'id': row[0],
                'filename': row[1],
                'original_filename': row[2],
                'file_path': row[3],
                'content': row[4][:200] + '...' if row[4] and len(row[4]) > 200 else row[4],
                'file_size': row[5],
                'upload_date': row[6],
                'description': row[7],
                'tags': row[8].split(',') if row[8] else []
            }
            documents.append(doc_data)
        
        return jsonify({
            'documents': documents
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@query_bp.route('/documents/<int:document_id>/summary', methods=['POST'])
def generate_document_summary(document_id):
    """Generate AI summary for a specific document"""
    try:
        import sqlite3
        import os
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'pdf_api.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, filename, content FROM document WHERE id = ?
        """, (document_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Document not found'}), 404
        
        document_content = row[2]
        
        if not document_content:
            return jsonify({
                'error': 'Document has no readable content',
                'summary': None
            }), 400
        
        # Initialize LLM service
        llm_service = LLMService()
        
        if not llm_service.is_available():
            return jsonify({
                'error': 'AI service is not available',
                'summary': None
            }), 500
        
        # Generate summary
        summary = llm_service.generate_summary(document_content)
        
        return jsonify({
            'document_id': document_id,
            'filename': row[1],
            'summary': summary,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error generating summary: {str(e)}',
            'summary': None,
            'success': False
        }), 500

@query_bp.route('/documents/<int:document_id>/keywords', methods=['POST'])
def extract_document_keywords(document_id):
    """Extract keywords from a specific document"""
    try:
        import sqlite3
        import os
        
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'pdf_api.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, filename, content FROM document WHERE id = ?
        """, (document_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Document not found'}), 404
        
        document_content = row[2]
        
        if not document_content:
            return jsonify({
                'error': 'Document has no readable content',
                'keywords': []
            }), 400
        
        # Initialize LLM service
        llm_service = LLMService()
        
        if not llm_service.is_available():
            return jsonify({
                'error': 'AI service is not available',
                'keywords': []
            }), 500
        
        # Extract keywords
        keywords = llm_service.extract_keywords(document_content)
        
        return jsonify({
            'document_id': document_id,
            'filename': row[1],
            'keywords': keywords,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error extracting keywords: {str(e)}',
            'keywords': [],
            'success': False
        }), 500
