"""
Enhanced file validation and security utilities
"""
import os
import magic
import hashlib
from werkzeug.utils import secure_filename
from flask import current_app

class FileValidator:
    """Enhanced file validation with multiple security checks"""
    
    ALLOWED_EXTENSIONS = {'pdf'}
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'application/x-pdf',
        'application/x-bzpdf',
        'application/x-gzpdf'
    }
    MAX_FILENAME_LENGTH = 100
    
    @staticmethod
    def validate_file(file, filename):
        """
        Comprehensive file validation
        
        Args:
            file: File object from request
            filename: Original filename
            
        Returns:
            tuple: (is_valid, error_message, secure_filename)
        """
        
        # Check if filename exists
        if not filename or filename == '':
            return False, "No filename provided", None
            
        # Check filename length
        if len(filename) > FileValidator.MAX_FILENAME_LENGTH:
            return False, "Filename too long", None
            
        # Secure the filename
        safe_filename = secure_filename(filename)
        if not safe_filename:
            return False, "Invalid filename", None
            
        # Check file extension
        if not FileValidator._has_allowed_extension(safe_filename):
            return False, "File type not allowed. Only PDF files are permitted", None
            
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        max_size = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
        if file_size > max_size:
            return False, f"File too large. Maximum size: {max_size // (1024*1024)}MB", None
            
        if file_size == 0:
            return False, "Empty file not allowed", None
            
        # Validate MIME type
        if not FileValidator._validate_mime_type(file):
            return False, "Invalid file type. File content doesn't match PDF format", None
            
        return True, None, safe_filename
    
    @staticmethod
    def _has_allowed_extension(filename):
        """Check if file has allowed extension"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileValidator.ALLOWED_EXTENSIONS
    
    @staticmethod
    def _validate_mime_type(file):
        """Validate file MIME type using python-magic"""
        try:
            # Read first 2048 bytes for MIME detection
            file_header = file.read(2048)
            file.seek(0)  # Reset file pointer
            
            # Use python-magic to detect MIME type
            mime_type = magic.from_buffer(file_header, mime=True)
            return mime_type in FileValidator.ALLOWED_MIME_TYPES
            
        except Exception:
            # If magic fails, fall back to basic extension check
            return True
    
    @staticmethod
    def generate_secure_filename(original_filename):
        """Generate a secure, unique filename"""
        safe_name = secure_filename(original_filename)
        
        # Add timestamp and hash for uniqueness
        import time
        timestamp = str(int(time.time() * 1000))
        
        # Create hash of original filename for additional uniqueness
        file_hash = hashlib.md5(original_filename.encode()).hexdigest()[:8]
        
        # Split filename and extension
        name, ext = os.path.splitext(safe_name)
        
        return f"{timestamp}_{file_hash}_{name}{ext}"

class PathValidator:
    """Validate and sanitize file paths"""
    
    @staticmethod
    def is_safe_path(base_dir, filename):
        """
        Check if the resolved path is within the base directory
        Prevents path traversal attacks
        """
        try:
            base_dir = os.path.abspath(base_dir)
            file_path = os.path.abspath(os.path.join(base_dir, filename))
            
            # Check if the file path starts with base directory
            return file_path.startswith(base_dir)
        except Exception:
            return False
    
    @staticmethod
    def sanitize_path(base_dir, filename):
        """Sanitize and validate file path"""
        safe_filename = secure_filename(filename)
        
        if not PathValidator.is_safe_path(base_dir, safe_filename):
            raise ValueError("Invalid file path detected")
            
        return os.path.join(base_dir, safe_filename)
