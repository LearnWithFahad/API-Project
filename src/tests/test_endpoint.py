#!/usr/bin/env python3
"""
Test the documents endpoint directly
"""

import requests
import json

def test_documents_endpoint():
    """Test the documents API endpoint"""
    
    print("🧪 Testing Documents Endpoint")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Test the documents endpoint
        print("📡 Testing GET /api/documents...")
        response = requests.get(f"{base_url}/api/documents", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"📊 Documents found: {data.get('total', 0)}")
            if data.get('documents'):
                for doc in data['documents']:
                    print(f"  - {doc.get('original_filename', 'Unknown')}")
        else:
            print(f"\n❌ ERROR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error message: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"Raw error: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the server running?")
    except requests.exceptions.Timeout:
        print("❌ Request timeout")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_documents_endpoint()
