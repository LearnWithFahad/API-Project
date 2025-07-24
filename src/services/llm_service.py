"""
Large Language Model service for AI-powered document querying
Updated to use Google's Gemini API
"""
import os
import json
import requests
from flask import current_app

class LLMService:
    """Service for interacting with Google's Gemini models"""
    
    def __init__(self):
        """Initialize Gemini client"""
        self.api_key = None
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Gemini client with API key"""
        try:
            # Try to get API key from current app config or environment
            api_key = None
            
            try:
                api_key = current_app.config.get('GEMINI_API_KEY')
            except RuntimeError:
                # If not in app context, get from environment
                pass
            
            if not api_key:
                api_key = os.environ.get('GEMINI_API_KEY')
            
            if not api_key:
                api_key = 'AIzaSyCpzRvQzcK4B2FWkCIPrc9Kf1-pN6jGfK8'  # Fallback to provided key
            
            self.api_key = api_key
            print("✅ Gemini client initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize Gemini client: {e}")
            self.api_key = None
    
    def is_available(self):
        """Check if LLM service is available"""
        return self.api_key is not None
    
    def _make_gemini_request(self, prompt, max_tokens=500, retry_count=3):
        """Make a request to Gemini API with retry logic"""
        if not self.is_available():
            return "AI service is not available. Please check Gemini API key configuration."
        
        import time
        
        for attempt in range(retry_count):
            try:
                url = f"{self.base_url}?key={self.api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }],
                    "generationConfig": {
                        "maxOutputTokens": max_tokens,
                        "temperature": 0.7,
                        "topP": 0.8,
                        "topK": 40
                    }
                }
                
                headers = {
                    "Content-Type": "application/json"
                }
                
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'candidates' in result and len(result['candidates']) > 0:
                        return result['candidates'][0]['content']['parts'][0]['text']
                    else:
                        return "No response generated from Gemini API."
                
                elif response.status_code == 503:
                    # Service unavailable - retry after delay
                    print(f"Gemini API overloaded (attempt {attempt + 1}/{retry_count}). Retrying in {2 ** attempt} seconds...")
                    if attempt < retry_count - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        return "🤖 Gemini AI is currently experiencing high traffic. Please try again in a few minutes. The service should be available shortly."
                
                elif response.status_code == 429:
                    # Rate limit - retry after delay
                    print(f"Rate limited (attempt {attempt + 1}/{retry_count}). Retrying...")
                    if attempt < retry_count - 1:
                        time.sleep(5)
                        continue
                    else:
                        return "API rate limit exceeded. Please wait a moment before trying again."
                
                else:
                    print(f"Gemini API error: {response.status_code} - {response.text}")
                    return f"Gemini API returned error {response.status_code}. Please try again later."
                    
            except requests.exceptions.Timeout:
                print(f"Request timeout (attempt {attempt + 1}/{retry_count})")
                if attempt < retry_count - 1:
                    time.sleep(2)
                    continue
                else:
                    return "Request timed out. Please check your internet connection and try again."
                    
            except Exception as e:
                print(f"Error making Gemini request (attempt {attempt + 1}/{retry_count}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(1)
                    continue
                else:
                    return f"Unable to connect to Gemini API: {str(e)}"
        
        return "Failed to get response after multiple attempts. Please try again later."
    
    def _provide_fallback_response(self, query, context):
        """Provide a basic fallback response when AI is unavailable"""
        # Simple keyword matching for basic responses
        query_lower = query.lower()
        context_lower = context.lower()
        
        # Basic keyword search
        if any(word in query_lower for word in ['summary', 'summarize', 'what is', 'about']):
            # Try to extract first few sentences as a basic summary
            sentences = context[:500].split('.')[:3]
            return f"Based on the document content: {'. '.join(sentences)}..."
        
        elif any(word in query_lower for word in ['title', 'name', 'document']):
            return "I can see document content is available, but AI processing is currently unavailable. Please try again later when the service is restored."
        
        elif any(word in query_lower for word in ['length', 'size', 'how long', 'how many']):
            char_count = len(context)
            word_count = len(context.split())
            return f"Document statistics: approximately {word_count} words and {char_count} characters."
        
        else:
            return f"I can see your question '{query}' relates to the document content, but AI processing is temporarily unavailable due to high demand. Please try again in a few minutes."

    def query_content(self, query, context, max_tokens=500):
        """Query content using Gemini LLM with fallback"""
        if not self.is_available():
            return self._provide_fallback_response(query, context)
        
        try:
            # Prepare prompt
            prompt = f"""Based on the following document content, please answer the user's question.

Document Content:
{context[:4000]}

User Question: {query}

Please provide a clear, concise answer based on the document content. If the answer cannot be found in the document, please say so."""

            response = self._make_gemini_request(prompt, max_tokens)
            
            # If response indicates API issues, provide fallback
            if any(phrase in response.lower() for phrase in ['overloaded', 'high traffic', 'try again', 'unavailable']):
                return f"🤖 {response}\n\n📄 **Fallback Info**: {self._provide_fallback_response(query, context)}"
            
            return response
            
        except Exception as e:
            print(f"Error in query_content: {e}")
            return self._provide_fallback_response(query, context)
    
    def generate_summary(self, content, max_tokens=300):
        """Generate summary of document content"""
        if not self.is_available():
            return "AI service is not available. Please check Gemini API key configuration."
        
        try:
            prompt = f"""Please provide a concise summary of the following document content:

{content[:4000]}

Summary should be informative and capture the main points of the document."""

            return self._make_gemini_request(prompt, max_tokens)
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Error generating summary: {str(e)}"
    
    def extract_keywords(self, content, max_tokens=100):
        """Extract keywords from document content"""
        if not self.is_available():
            return []
        
        try:
            prompt = f"""Extract the most important keywords and phrases from the following document content. Return them as a comma-separated list:

{content[:4000]}

Keywords:"""

            response = self._make_gemini_request(prompt, max_tokens)
            
            # Parse the response to extract keywords
            if response and "Error" not in response:
                keywords = [keyword.strip() for keyword in response.split(',')]
                return keywords[:10]  # Limit to 10 keywords
            else:
                return []
                
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
    
    def get_model_info(self):
        """Get information about the current model"""
        return {
            "provider": "Google",
            "model": "Gemini Pro",
            "api_url": self.base_url,
            "available": self.is_available()
        }
