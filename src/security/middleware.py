"""
Enhanced security configuration and middleware
"""
import os
import secrets
from functools import wraps
from flask import request, jsonify, current_app, session
from datetime import datetime, timedelta

class SecurityConfig:
    """Enhanced security configuration"""
    
    # Session security
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # File upload security
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_EXTENSIONS = {'pdf'}
    
    # Rate limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 60  # minutes
    
    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }

def generate_secure_key():
    """Generate a secure secret key"""
    return secrets.token_urlsafe(32)

def require_api_key(f):
    """Decorator to require API key for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        # In production, validate against stored API keys
        valid_api_key = current_app.config.get('API_KEY')
        
        if not api_key or api_key != valid_api_key:
            return jsonify({'error': 'Invalid or missing API key'}), 401
            
        return f(*args, **kwargs)
    return decorated_function

def log_security_event(event_type, details, ip_address):
    """Log security events"""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] SECURITY: {event_type} from {ip_address} - {details}"
    
    # In production, use proper logging
    print(log_entry)
    
    # Could also write to file or send alerts
    security_log_file = "security.log"
    try:
        with open(security_log_file, 'a') as f:
            f.write(log_entry + "\n")
    except Exception:
        pass

def get_client_ip():
    """Get real client IP address"""
    # Check for forwarded headers (be careful with these in production)
    if 'X-Forwarded-For' in request.headers:
        return request.headers['X-Forwarded-For'].split(',')[0].strip()
    elif 'X-Real-IP' in request.headers:
        return request.headers['X-Real-IP']
    else:
        return request.remote_addr

class SecurityMiddleware:
    """Security middleware for Flask application"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security middleware"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        
        # Set secure session configuration
        app.config.update(
            SESSION_COOKIE_SECURE=SecurityConfig.SESSION_COOKIE_SECURE,
            SESSION_COOKIE_HTTPONLY=SecurityConfig.SESSION_COOKIE_HTTPONLY,
            SESSION_COOKIE_SAMESITE=SecurityConfig.SESSION_COOKIE_SAMESITE,
            PERMANENT_SESSION_LIFETIME=SecurityConfig.PERMANENT_SESSION_LIFETIME
        )
    
    def before_request(self):
        """Process request before handling"""
        
        # Block suspicious requests
        if self._is_suspicious_request():
            log_security_event(
                "BLOCKED_REQUEST", 
                f"Suspicious request to {request.path}",
                get_client_ip()
            )
            return jsonify({'error': 'Request blocked'}), 403
        
        # Validate content length
        if request.content_length:
            max_length = current_app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
            if request.content_length > max_length:
                return jsonify({'error': 'Request too large'}), 413
    
    def after_request(self, response):
        """Process response after handling"""
        
        # Add security headers
        for header, value in SecurityConfig.SECURITY_HEADERS.items():
            response.headers[header] = value
        
        # Remove server information
        response.headers.pop('Server', None)
        
        return response
    
    def _is_suspicious_request(self):
        """Check for suspicious request patterns"""
        
        # Check for common attack patterns in URL
        suspicious_patterns = [
            '../', '..\\', '/etc/', '/proc/', '/sys/',
            '<script', 'javascript:', 'vbscript:',
            'union select', 'drop table', 'insert into'
        ]
        
        request_path = request.path.lower()
        for pattern in suspicious_patterns:
            if pattern in request_path:
                return True
        
        # Check query parameters
        for arg in request.args.values():
            arg_lower = arg.lower()
            for pattern in suspicious_patterns:
                if pattern in arg_lower:
                    return True
        
        return False
