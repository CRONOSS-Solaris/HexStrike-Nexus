"""
Google Gemini Provider
"""
import requests
import json
from typing import List, Dict, Optional, Generator
from ..ai_provider_base import AIProviderBase


class GeminiProvider(AIProviderBase):
    """Google Gemini AI provider implementation"""
    
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    STREAM_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent"
    
    def __init__(self, api_key: str, model: str = "gemini-pro", **kwargs):
        super().__init__(api_key, model, **kwargs)
        
    def chat_completion(self, messages: List[Dict[str, str]], 
                       system_prompt: Optional[str] = None,
                       **kwargs) -> str:
        """Send chat completion request to Google Gemini"""
        
        # Build the URL with model and API key
        url = self.API_URL.format(model=self.model)
        params = {"key": self.api_key}
        
        # Convert messages to Gemini format
        gemini_contents = self._convert_messages_to_gemini(messages, system_prompt)
        
        data = {
            "contents": gemini_contents,
            "generationConfig": {
                "temperature": kwargs.get('temperature', 0.7),
                "maxOutputTokens": kwargs.get('max_tokens', 8192),
            }
        }
        
        try:
            response = requests.post(url, params=params, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract text from Gemini response
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    return ''.join(part.get('text', '') for part in parts)
            
            raise Exception("No valid response from Gemini")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Gemini API error: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response format from Gemini: {str(e)}")
    
    def stream_completion(self, messages: List[Dict[str, str]], 
                         system_prompt: Optional[str] = None,
                         **kwargs) -> Generator[str, None, None]:
        """Stream chat completion from Google Gemini"""
        
        # Build the URL with model and API key
        url = self.STREAM_URL.format(model=self.model)
        params = {"key": self.api_key, "alt": "sse"}
        
        # Convert messages to Gemini format
        gemini_contents = self._convert_messages_to_gemini(messages, system_prompt)
        
        data = {
            "contents": gemini_contents,
            "generationConfig": {
                "temperature": kwargs.get('temperature', 0.7),
                "maxOutputTokens": kwargs.get('max_tokens', 8192),
            }
        }
        
        try:
            response = requests.post(url, params=params, json=data, 
                                   stream=True, timeout=60)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        data_str = line_text[6:]
                        try:
                            chunk = json.loads(data_str)
                            if 'candidates' in chunk and len(chunk['candidates']) > 0:
                                candidate = chunk['candidates'][0]
                                if 'content' in candidate and 'parts' in candidate['content']:
                                    parts = candidate['content']['parts']
                                    text = ''.join(part.get('text', '') for part in parts)
                                    if text:
                                        yield text
                        except json.JSONDecodeError:
                            continue
                            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Gemini streaming error: {str(e)}")
    
    def validate_connection(self) -> bool:
        """Test Gemini connection"""
        try:
            test_messages = [{"role": "user", "content": "Hi"}]
            response = self.chat_completion(test_messages, max_tokens=10)
            return bool(response)
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available Gemini models"""
        # Return default Gemini models
        return [
            "gemini-1.5-pro-latest",
            "gemini-1.5-flash-latest",
            "gemini-pro",
            "gemini-pro-vision"
        ]
    
    def _convert_messages_to_gemini(self, messages: List[Dict[str, str]], 
                                   system_prompt: Optional[str] = None) -> List[Dict]:
        """
        Convert standard messages format to Gemini format
        
        Gemini uses a different format:
        - role: 'user' or 'model' (not 'assistant')
        - parts: [{"text": "content"}]
        """
        gemini_contents = []
        
        # Add system prompt as first user message if provided
        if system_prompt:
            gemini_contents.append({
                "role": "user",
                "parts": [{"text": f"System instructions: {system_prompt}"}]
            })
            gemini_contents.append({
                "role": "model",
                "parts": [{"text": "Understood. I will follow these instructions."}]
            })
        
        # Convert messages
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            
            # Map 'assistant' to 'model' for Gemini
            if role == 'assistant':
                role = 'model'
            elif role == 'system':
                # Treat system messages as user messages
                role = 'user'
                content = f"System: {content}"
            
            gemini_contents.append({
                "role": role,
                "parts": [{"text": content}]
            })
        
        return gemini_contents
