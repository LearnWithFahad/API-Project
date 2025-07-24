#!/usr/bin/env python3
"""Test LLM service within Flask app context"""
from app_simple import create_app
from services.llm_service import LLMService

def test_llm_service():
    app = create_app()
    with app.app_context():
        llm = LLMService()
        print(f'✅ LLM Service in app context: {llm.is_available()}')
        
        if llm.is_available():
            try:
                result = llm.query_content(
                    query="What is artificial intelligence?",
                    context="AI is a field of computer science.",
                    max_tokens=50
                )
                print(f'✅ Test query result: {result[:100]}...')
            except Exception as e:
                print(f'❌ Test query failed: {e}')

if __name__ == '__main__':
    test_llm_service()
