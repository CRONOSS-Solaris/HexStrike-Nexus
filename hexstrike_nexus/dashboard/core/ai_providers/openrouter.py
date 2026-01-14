"""
OpenRouter AI Provider
Supports multiple models through OpenRouter API
"""
import requests
import json
from typing import List, Dict, Optional, Generator
from ..ai_provider_base import AIProviderBase


class OpenRouterProvider(AIProviderBase):
    """OpenRouter AI provider implementation"""
    
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODELS_URL = "https://openrouter.ai/api/v1/models"
    
    def __init__(self, api_key: str, model: str = "anthropic/claude-3.5-sonnet", **kwargs):
        super().__init__(api_key, model, **kwargs)
        self.app_name = kwargs.get('app_name', 'HexStrike-Nexus')
        
    def chat_completion(self, messages: List[Dict[str, str]], 
                       system_prompt: Optional[str] = None,
                       **kwargs) -> str:
        """Send chat completion request to OpenRouter"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/hexstrike-nexus",
            "X-Title": self.app_name,
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
            raise Exception(f"OpenRouter API error: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response format from OpenRouter: {str(e)}")
    
    def stream_completion(self, messages: List[Dict[str, str]], 
                         system_prompt: Optional[str] = None,
                         **kwargs) -> Generator[str, None, None]:
        """Stream chat completion from OpenRouter"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/hexstrike-nexus",
            "X-Title": self.app_name,
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
            raise Exception(f"OpenRouter streaming error: {str(e)}")
    
    def validate_connection(self) -> bool:
        """Test OpenRouter connection"""
        try:
            test_messages = [{"role": "user", "content": "Hi"}]
            response = self.chat_completion(test_messages, max_tokens=10)
            return bool(response)
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models from OpenRouter"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            response = requests.get(self.MODELS_URL, headers=headers, timeout=10)
            response.raise_for_status()
            
            models_data = response.json()
            return [model['id'] for model in models_data.get('data', [])]
        except Exception:
            # Return popular defaults if API call fails
            return [
                "anthropic/claude-3.5-sonnet",
                "anthropic/claude-3-opus",
                "openai/gpt-4-turbo",
                "openai/gpt-4o",
                "google/gemini-pro",
                "meta-llama/llama-3.1-70b-instruct"
            ]
