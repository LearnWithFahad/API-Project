from datetime import datetime

# Import db from app module - this will work after app initialization
def get_db():
    from app import db
    return db

class Document:
    """Document model for storing PDF information and content"""
    
    def __init__(self):
        # Initialize table when db is available
        pass
    
    @classmethod
    def create_table(cls, db):
        """Create the document table with SQLAlchemy"""
        class DocumentModel(db.Model):
            __tablename__ = 'document'
            
            id = db.Column(db.Integer, primary_key=True)
            filename = db.Column(db.String(255), nullable=False)
            original_filename = db.Column(db.String(255), nullable=False)
            file_path = db.Column(db.String(500), nullable=False)
            content = db.Column(db.Text, nullable=True)  # Extracted text content
            file_size = db.Column(db.Integer, nullable=False)
            upload_date = db.Column(db.DateTime, default=datetime.utcnow)
            description = db.Column(db.Text, nullable=True)
            tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags
            
            def __repr__(self):
                return f'<Document {self.filename}>'
            
            def to_dict(self):
                """Convert document to dictionary for JSON serialization"""
                return {
                    'id': self.id,
                    'filename': self.filename,
                    'original_filename': self.original_filename,
                    'file_path': self.file_path,
                    'content': self.content,
                    'file_size': self.file_size,
                    'upload_date': self.upload_date.isoformat() if self.upload_date else None,
                    'description': self.description,
                    'tags': self.tags.split(',') if self.tags else []
                }
        
        return DocumentModel
