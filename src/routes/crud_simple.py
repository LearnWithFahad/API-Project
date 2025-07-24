from flask import Blueprint, request, jsonify, current_app, g

crud_bp = Blueprint('crud', __name__)

def get_db_and_model():
    """Get database and model from current app"""
    from flask import current_app
    
    # Get the db instance from current app without extra context
    from app_simple import db, Document
    return db, Document

@crud_bp.route('/documents', methods=['GET'])
def list_documents():
    """List all documents"""
    try:
        # Get database components
        db, Document = get_db_and_model()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query all documents first
        all_documents = Document.query.all()
        
        # Manual pagination
        start = (page - 1) * per_page
        end = start + per_page
        documents = all_documents[start:end]
        
        total = len(all_documents)
        pages = (total + per_page - 1) // per_page if total > 0 else 1
        
        return jsonify({
            'documents': [doc.to_dict() for doc in documents],
            'total': total,
            'page': page,
            'pages': pages,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        error_msg = str(e)
        current_app.logger.error(f"Error listing documents: {error_msg}")
        return jsonify({'error': error_msg}), 500

@crud_bp.route('/documents/<int:document_id>', methods=['GET'])
def get_document(document_id):
    """Get a specific document"""
    try:
        db, Document = get_db_and_model()
        document = Document.query.get(document_id)
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
            
        return jsonify({
            'document': document.to_dict()
        }), 200
        
    except Exception as e:
        error_msg = str(e)
        current_app.logger.error(f"Error getting document {document_id}: {error_msg}")
        return jsonify({'error': error_msg}), 500

@crud_bp.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    """Delete a document"""
    try:
        db, Document = get_db_and_model()
        document = Document.query.get(document_id)
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Delete file from filesystem
        import os
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Document deleted successfully'
        }), 200
        
    except Exception as e:
        error_msg = str(e)
        current_app.logger.error(f"Error deleting document {document_id}: {error_msg}")
        return jsonify({'error': error_msg}), 500

@crud_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get document statistics"""
    try:
        db, Document = get_db_and_model()
        documents = Document.query.all()
        
        total_docs = len(documents)
        total_size = sum(doc.file_size for doc in documents)
        total_size_mb = round(total_size / (1024 * 1024), 2) if total_size > 0 else 0
        
        return jsonify({
            'total_documents': total_docs,
            'total_size_bytes': total_size,
            'total_size_mb': total_size_mb
        }), 200
        
    except Exception as e:
        error_msg = str(e)
        current_app.logger.error(f"Error getting stats: {error_msg}")
        return jsonify({'error': error_msg}), 500
