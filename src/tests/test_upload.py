#!/usr/bin/env python3
"""Test upload endpoint with a simple PDF"""
import requests
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_test_pdf():
    """Create a simple test PDF in memory"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Test PDF Document")
    p.drawString(100, 730, "This is a simple test PDF for upload testing.")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def test_upload():
    """Test the upload endpoint"""
    try:
        # Create test PDF
        pdf_buffer = create_test_pdf()
        
        # Prepare the upload
        files = {
            'file': ('test_document.pdf', pdf_buffer, 'application/pdf')
        }
        
        # Make the request
        response = requests.post('http://127.0.0.1:5000/api/upload', files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_upload()
