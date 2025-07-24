#!/usr/bin/env python3
"""
Security Setup Script for PDF API
Run this to set up security configurations
"""

import os
import secrets
import shutil
from pathlib import Path

def generate_secure_env():
    """Generate a secure .env file"""
    print("🔒 Generating secure environment configuration...")
    
    # Generate secure keys
    secret_key = secrets.token_urlsafe(32)
    api_key = secrets.token_urlsafe(32)
    
    env_content = f"""# Security Environment Configuration
# Generated on {__import__('datetime').datetime.now().isoformat()}

# Application Settings
FLASK_ENV=development
SECRET_KEY={secret_key}
API_KEY={api_key}

# Database
DATABASE_URL=sqlite:///pdf_api.db

# OpenAI API (add your key here)
OPENAI_API_KEY=your-openai-api-key-here

# Security Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5000,http://127.0.0.1:5000

# File Upload Settings
MAX_FILE_SIZE=16777216  # 16MB in bytes
UPLOAD_FOLDER=uploads

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600  # 1 hour in seconds

# Session Security
SESSION_TIMEOUT=7200  # 2 hours in seconds

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# Production Only Settings (uncomment for production)
# PREFERRED_URL_SCHEME=https
# SESSION_COOKIE_SECURE=true
# WTF_CSRF_ENABLED=true
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created with secure keys")
    print(f"   Secret Key: {secret_key[:10]}...")
    print(f"   API Key: {api_key[:10]}...")
    print("   ⚠️  Remember to add your OpenAI API key!")

def create_security_directories():
    """Create necessary security directories"""
    print("📁 Creating security directories...")
    
    directories = [
        'uploads',
        'logs',
        'security'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ Created: {directory}/")

def set_file_permissions():
    """Set secure file permissions (Unix/Linux only)"""
    if os.name == 'posix':  # Unix/Linux
        print("🔐 Setting file permissions...")
        
        # Set restrictive permissions on sensitive files
        sensitive_files = ['.env', 'pdf_api.db']
        
        for file_path in sensitive_files:
            if os.path.exists(file_path):
                os.chmod(file_path, 0o600)  # Read/write for owner only
                print(f"   ✅ Secured: {file_path}")
        
        # Set directory permissions
        os.chmod('uploads', 0o755)  # rwxr-xr-x
        print("   ✅ Secured: uploads/ directory")
    else:
        print("⚠️  File permissions not set (Windows detected)")
        print("   Manually secure sensitive files through file properties")

def check_dependencies():
    """Check if security dependencies are installed"""
    print("📦 Checking security dependencies...")
    
    required_packages = [
        'flask',
        'flask-sqlalchemy',
        'python-magic',
        'werkzeug',
        'cryptography',
        'flask-limiter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install " + " ".join(missing_packages))
        return False
    
    return True

def create_security_checklist():
    """Create a security checklist file"""
    print("📋 Creating security checklist...")
    
    checklist = """# Security Checklist for PDF API

## Pre-Deployment Security
- [ ] Changed default secret keys (.env file)
- [ ] Added OpenAI API key to .env
- [ ] Reviewed and configured CORS origins
- [ ] Set up proper file permissions
- [ ] Installed all security dependencies
- [ ] Tested file upload restrictions
- [ ] Verified rate limiting works
- [ ] Checked error handling doesn't leak info

## Production Deployment
- [ ] Set FLASK_ENV=production
- [ ] Enable HTTPS/TLS
- [ ] Configure reverse proxy (nginx/Apache)
- [ ] Set up firewall rules
- [ ] Configure database backups
- [ ] Set up logging and monitoring
- [ ] Remove debug mode
- [ ] Set secure session cookies

## Regular Maintenance
- [ ] Update dependencies monthly
- [ ] Review security logs weekly
- [ ] Rotate API keys quarterly
- [ ] Run security tests regularly
- [ ] Monitor for vulnerabilities
- [ ] Test backup restoration

## Security Testing
Run the security test script:
```bash
python security_test.py
```

## Security Monitoring
- Check security.log for suspicious activity
- Monitor app.log for errors
- Review file upload patterns
- Watch for rate limiting triggers

## Emergency Response
If you detect an attack:
1. Block malicious IP addresses
2. Review recent logs
3. Check data integrity
4. Update security measures
5. Restore from backups if needed

Remember: Security is an ongoing process!
"""
    
    with open('SECURITY_CHECKLIST.md', 'w') as f:
        f.write(checklist)
    
    print("   ✅ Created: SECURITY_CHECKLIST.md")

def main():
    """Main setup function"""
    print("🚀 PDF API Security Setup")
    print("=" * 40)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return
    
    # Create directories
    create_security_directories()
    
    # Generate secure configuration
    generate_secure_env()
    
    # Set file permissions
    set_file_permissions()
    
    # Create checklist
    create_security_checklist()
    
    print("\n" + "=" * 40)
    print("✅ Security setup completed!")
    print("\nNext steps:")
    print("1. Review and edit .env file")
    print("2. Add your OpenAI API key")
    print("3. Run: python security_test.py")
    print("4. Check SECURITY_CHECKLIST.md")
    print("5. Start your application securely!")
    print("\n🔒 Your application is now more secure!")

if __name__ == "__main__":
    main()
