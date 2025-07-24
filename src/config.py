import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Generate secure secret key if not provided
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///pdf_api.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload security
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # API Security
    API_KEY = os.environ.get('API_KEY') or secrets.token_urlsafe(32)
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'AIzaSyCpzRvQzcK4B2FWkCIPrc9Kf1-pN6jGfK8'
    
    # Session security
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = 'memory://'
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def init_app(app):
        """Initialize application with security settings"""
        
        # Ensure upload directory exists with proper permissions
        upload_path = os.path.abspath(Config.UPLOAD_FOLDER)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, mode=0o755)
            
        # Set up logging
        import logging
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s %(levelname)s: %(message)s'
        )

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Require HTTPS in production
    
    # Additional production security
    PREFERRED_URL_SCHEME = 'https'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Log to file in production
        import logging
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler(
            'app.log', maxBytes=10240000, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
