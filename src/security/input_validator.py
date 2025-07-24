"""
Input validation and sanitization utilities
"""
import re
import html
import bleach
from markupsafe import Markup

class InputValidator:
    """Input validation and sanitization"""
    
    # Common patterns
    FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')
    TAG_PATTERN = re.compile(r'^[a-zA-Z0-9,\s._-]+$')
    
    # Allowed HTML tags for descriptions (very restrictive)
    ALLOWED_TAGS = ['p', 'br', 'strong', 'em']
    ALLOWED_ATTRIBUTES = {}
    
    @staticmethod
    def sanitize_html(text):
        """Sanitize HTML content"""
        if not text:
            return ""
            
        # Use bleach to clean HTML
        cleaned = bleach.clean(
            text,
            tags=InputValidator.ALLOWED_TAGS,
            attributes=InputValidator.ALLOWED_ATTRIBUTES,
            strip=True
        )
        
        return cleaned
    
    @staticmethod
    def sanitize_text(text, max_length=1000):
        """Sanitize plain text input"""
        if not text:
            return ""
            
        # Escape HTML entities
        sanitized = html.escape(text.strip())
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
            
        return sanitized
    
    @staticmethod
    def validate_tags(tags):
        """Validate and sanitize tags"""
        if not tags:
            return ""
            
        # Remove extra whitespace and split
        tag_list = [tag.strip() for tag in tags.split(',')]
        
        # Validate each tag
        valid_tags = []
        for tag in tag_list:
            if tag and InputValidator.TAG_PATTERN.match(tag) and len(tag) <= 50:
                valid_tags.append(html.escape(tag))
                
        return ','.join(valid_tags)
    
    @staticmethod
    def validate_description(description):
        """Validate and sanitize description"""
        if not description:
            return ""
            
        # Limit length
        if len(description) > 2000:
            description = description[:2000]
            
        return InputValidator.sanitize_html(description)
    
    @staticmethod
    def validate_query(query):
        """Validate search/query input"""
        if not query:
            return None, "Query cannot be empty"
            
        # Sanitize query
        sanitized_query = InputValidator.sanitize_text(query, max_length=500)
        
        if len(sanitized_query.strip()) < 3:
            return None, "Query must be at least 3 characters long"
            
        return sanitized_query, None

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self._requests = {}
        self._blocked_ips = set()
    
    def is_allowed(self, ip_address, max_requests=100, window_minutes=60):
        """
        Check if request from IP is allowed
        
        Args:
            ip_address: Client IP address
            max_requests: Maximum requests per window
            window_minutes: Time window in minutes
            
        Returns:
            bool: True if allowed, False if rate limited
        """
        import time
        
        current_time = time.time()
        window_start = current_time - (window_minutes * 60)
        
        # Check if IP is blocked
        if ip_address in self._blocked_ips:
            return False
        
        # Get requests for this IP in current window
        if ip_address not in self._requests:
            self._requests[ip_address] = []
            
        # Clean old requests
        self._requests[ip_address] = [
            req_time for req_time in self._requests[ip_address]
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self._requests[ip_address]) >= max_requests:
            # Block IP for repeated violations
            if len(self._requests[ip_address]) > max_requests * 2:
                self._blocked_ips.add(ip_address)
            return False
            
        # Add current request
        self._requests[ip_address].append(current_time)
        return True
