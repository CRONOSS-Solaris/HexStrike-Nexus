"""
Anthropic (Claude) Provider
"""
import requests
import json
from typing import List, Dict, Optional, Generator
from ..ai_provider_base import AIProviderBase


class AnthropicProvider(AIProviderBase):
    """Anthropic Claude provider implementation"""
    
    API_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", **kwargs):
        super().__init__(api_key, model, **kwargs)
        
    def _convert_messages(self, messages: List[Dict[str, str]], 
                         system_prompt: Optional[str] = None) -> tuple:
        """
        Convert standard messages to Anthropic format
        Anthropic uses separate system parameter, not in messages array
        """
        anthropic_messages = []
        
        for msg in messages:
            if msg['role'] != 'system':
                anthropic_messages.append(msg)
        
        return anthropic_messages, system_prompt
        
    def chat_completion(self, messages: List[Dict[str, str]], 
                       system_prompt: Optional[str] = None,
                       **kwargs) -> str:
        """Send chat completion request to Anthropic"""
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.API_VERSION,
            "Content-Type": "application/json"
        }
        
        anthropic_messages, system = self._convert_messages(messages, system_prompt)
        
        data = {
            "model": self.model,
            "messages": anthropic_messages,
            "max_tokens": kwargs.get('max_tokens', 4000),
            "temperature": kwargs.get('temperature', 0.7),
        }
        
        if system:
            data["system"] = system
        
        try:
            response = requests.post(self.API_URL, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result['content'][0]['text']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Anthropic API error: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response format from Anthropic: {str(e)}")
    
    def stream_completion(self, messages: List[Dict[str, str]], 
                         system_prompt: Optional[str] = None,
                         **kwargs) -> Generator[str, None, None]:
        """Stream chat completion from Anthropic"""
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.API_VERSION,
            "Content-Type": "application/json"
        }
        
        anthropic_messages, system = self._convert_messages(messages, system_prompt)
        
        data = {
            "model": self.model,
            "messages": anthropic_messages,
            "max_tokens": kwargs.get('max_tokens', 4000),
            "temperature": kwargs.get('temperature', 0.7),
            "stream": True
        }
        
        if system:
            data["system"] = system
        
        try:
            response = requests.post(self.API_URL, headers=headers, json=data, 
                                   stream=True, timeout=60)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        data_str = line_text[6:]
                        try:
                            chunk = json.loads(data_str)
                            if chunk.get('type') == 'content_block_delta':
                                delta = chunk.get('delta', {})
                                content = delta.get('text', '')
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
                            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Anthropic streaming error: {str(e)}")
    
    def validate_connection(self) -> bool:
        """Test Anthropic connection"""
        try:
            test_messages = [{"role": "user", "content": "Hi"}]
            response = self.chat_completion(test_messages, max_tokens=10)
            return bool(response)
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Return list of Anthropic models"""
        # Anthropic doesn't have a models endpoint, return known models
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
