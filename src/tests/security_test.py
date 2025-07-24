#!/usr/bin/env python3
"""
Security Testing Script for PDF API
Run this script to test various security measures
"""

import requests
import json
import time
import os
import sys
from pathlib import Path

class SecurityTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.session = requests.Session()
        
    def print_test_header(self, test_name):
        print(f"\n{'='*60}")
        print(f"Testing: {test_name}")
        print('='*60)
    
    def test_file_upload_security(self):
        """Test file upload security measures"""
        self.print_test_header("File Upload Security")
        
        # Test 1: Upload non-PDF file
        print("1. Testing non-PDF file upload...")
        try:
            files = {'file': ('test.txt', b'This is not a PDF', 'text/plain')}
            response = self.session.post(f"{self.api_url}/upload", files=files)
            if response.status_code == 400:
                print("✅ Non-PDF file correctly rejected")
            else:
                print(f"❌ Non-PDF file not rejected (status: {response.status_code})")
        except Exception as e:
            print(f"❌ Error testing non-PDF upload: {e}")
        
        # Test 2: Empty file upload
        print("2. Testing empty file upload...")
        try:
            files = {'file': ('', b'', 'application/pdf')}
            response = self.session.post(f"{self.api_url}/upload", files=files)
            if response.status_code == 400:
                print("✅ Empty file correctly rejected")
            else:
                print(f"❌ Empty file not rejected (status: {response.status_code})")
        except Exception as e:
            print(f"❌ Error testing empty file: {e}")
        
        # Test 3: File with malicious name
        print("3. Testing malicious filename...")
        try:
            malicious_name = "../../../etc/passwd.pdf"
            files = {'file': (malicious_name, b'%PDF-1.4 fake pdf', 'application/pdf')}
            response = self.session.post(f"{self.api_url}/upload", files=files)
            if response.status_code == 400 or (response.status_code == 201 and malicious_name not in response.text):
                print("✅ Malicious filename handled safely")
            else:
                print(f"❌ Malicious filename not handled properly")
        except Exception as e:
            print(f"❌ Error testing malicious filename: {e}")
    
    def test_rate_limiting(self):
        """Test rate limiting"""
        self.print_test_header("Rate Limiting")
        
        print("Testing rate limiting (this may take a moment)...")
        
        # Make rapid requests
        blocked = False
        for i in range(60):  # Try 60 requests rapidly
            try:
                response = self.session.get(f"{self.api_url}/documents")
                if response.status_code == 429:
                    print(f"✅ Rate limiting activated after {i+1} requests")
                    blocked = True
                    break
                time.sleep(0.1)  # Small delay
            except Exception as e:
                print(f"Error on request {i+1}: {e}")
                break
        
        if not blocked:
            print("⚠️  Rate limiting not activated (or limit is very high)")
    
    def test_input_validation(self):
        """Test input validation"""
        self.print_test_header("Input Validation")
        
        # Test XSS in description
        print("1. Testing XSS in description field...")
        try:
            xss_payload = "<script>alert('xss')</script>"
            files = {'file': ('test.pdf', b'%PDF-1.4 fake pdf', 'application/pdf')}
            data = {'description': xss_payload}
            response = self.session.post(f"{self.api_url}/upload", files=files, data=data)
            
            if response.status_code == 201:
                # Check if XSS payload was sanitized
                result = response.json()
                if '<script>' not in result.get('document', {}).get('description', ''):
                    print("✅ XSS payload sanitized")
                else:
                    print("❌ XSS payload not sanitized")
            else:
                print(f"Upload failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing XSS: {e}")
        
        # Test SQL injection in query
        print("2. Testing SQL injection in query...")
        try:
            sql_payload = "'; DROP TABLE documents; --"
            data = {'query': sql_payload}
            response = self.session.post(f"{self.api_url}/query", json=data)
            
            # If server is still responding, SQL injection likely prevented
            if response.status_code in [200, 400, 500]:
                print("✅ Server still responding after SQL injection attempt")
            else:
                print("⚠️  Unexpected response to SQL injection test")
        except Exception as e:
            print(f"❌ Error testing SQL injection: {e}")
    
    def test_security_headers(self):
        """Test security headers"""
        self.print_test_header("Security Headers")
        
        try:
            response = self.session.get(self.base_url)
            headers = response.headers
            
            required_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block'
            }
            
            for header, expected_value in required_headers.items():
                if header in headers:
                    if headers[header] == expected_value:
                        print(f"✅ {header}: {headers[header]}")
                    else:
                        print(f"⚠️  {header}: {headers[header]} (expected: {expected_value})")
                else:
                    print(f"❌ Missing header: {header}")
                    
        except Exception as e:
            print(f"❌ Error testing headers: {e}")
    
    def test_error_handling(self):
        """Test error handling doesn't leak information"""
        self.print_test_header("Error Handling")
        
        # Test 404 error
        print("1. Testing 404 error...")
        try:
            response = self.session.get(f"{self.api_url}/nonexistent")
            if response.status_code == 404:
                result = response.json()
                if 'error' in result and len(result['error']) < 100:  # Simple error message
                    print("✅ 404 error handled properly")
                else:
                    print("⚠️  404 error may leak information")
            else:
                print(f"Unexpected status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing 404: {e}")
        
        # Test invalid document ID
        print("2. Testing invalid document ID...")
        try:
            response = self.session.get(f"{self.api_url}/documents/99999")
            if response.status_code == 404:
                print("✅ Invalid document ID handled properly")
            else:
                print(f"Unexpected status for invalid ID: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing invalid ID: {e}")
    
    def run_all_tests(self):
        """Run all security tests"""
        print("🔒 Starting Security Tests for PDF API")
        print(f"Target: {self.base_url}")
        
        # Check if server is running
        try:
            response = self.session.get(self.base_url, timeout=5)
            if response.status_code != 200:
                print(f"❌ Server not responding properly (status: {response.status_code})")
                return
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            print("Make sure the server is running on the specified URL")
            return
        
        # Run tests
        self.test_security_headers()
        self.test_file_upload_security()
        self.test_input_validation()
        self.test_error_handling()
        self.test_rate_limiting()
        
        print(f"\n{'='*60}")
        print("Security testing completed!")
        print("Review the results above and address any issues marked with ❌ or ⚠️")
        print('='*60)

def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:5000"
    
    tester = SecurityTester(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
