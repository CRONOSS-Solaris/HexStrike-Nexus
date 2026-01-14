"""
OpenAI / ChatGPT Provider
"""
import requests
import json
from typing import List, Dict, Optional, Generator
from ..ai_provider_base import AIProviderBase


class OpenAIProvider(AIProviderBase):
    """OpenAI (ChatGPT) provider implementation"""
    
    API_URL = "https://api.openai.com/v1/chat/completions"
    MODELS_URL = "https://api.openai.com/v1/models"
    
    def __init__(self, api_key: str, model: str = "gpt-4o", **kwargs):
        super().__init__(api_key, model, **kwargs)
        
    def chat_completion(self, messages: List[Dict[str, str]], 
                       system_prompt: Optional[str] = None,
                       **kwargs) -> str:
        """Send chat completion request to OpenAI"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        formatted_messages = self.format_messages(messages, system_prompt)
        
        data = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 4000),
        }
        
        try:
            response = requests.post(self.API_URL, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API error: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response format from OpenAI: {str(e)}")
    
    def stream_completion(self, messages: List[Dict[str, str]], 
                         system_prompt: Optional[str] = None,
                         **kwargs) -> Generator[str, None, None]:
        """Stream chat completion from OpenAI"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        formatted_messages = self.format_messages(messages, system_prompt)
        
        data = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 4000),
            "stream": True
        }
        
        try:
            response = requests.post(self.API_URL, headers=headers, json=data, 
                                   stream=True, timeout=60)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        data_str = line_text[6:]
                        if data_str == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data_str)
                            if 'choices' in chunk and len(chunk['choices']) > 0:
                                delta = chunk['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
                            
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI streaming error: {str(e)}")
    
    def validate_connection(self) -> bool:
        """Test OpenAI connection"""
        try:
            test_messages = [{"role": "user", "content": "Hi"}]
            response = self.chat_completion(test_messages, max_tokens=10)
            return bool(response)
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models from OpenAI"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            response = requests.get(self.MODELS_URL, headers=headers, timeout=10)
            response.raise_for_status()
            
            models_data = response.json()
            # Filter for chat models only
            chat_models = [m['id'] for m in models_data.get('data', []) 
                          if 'gpt' in m['id'].lower()]
            return chat_models
        except Exception:
            # Return defaults if API call fails
            return [
                "gpt-4o",
                "gpt-4-turbo",
                "gpt-4",
                "gpt-3.5-turbo"
            ]
