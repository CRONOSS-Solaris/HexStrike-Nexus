"""
Base class for AI providers
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Generator


class AIProviderBase(ABC):
    """Abstract base class for all AI providers"""
    
    def __init__(self, api_key: str, model: str, **kwargs):
        """
        Initialize AI provider with credentials
        
        Args:
            api_key: API key for the provider
            model: Model identifier
            **kwargs: Additional provider-specific configuration
        """
        self.api_key = api_key
        self.model = model
        self.config = kwargs
        
    @abstractmethod
    def chat_completion(self, messages: List[Dict[str, str]], 
                       system_prompt: Optional[str] = None,
                       **kwargs) -> str:
        """
        Send chat completion request and return response
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt to prepend
            **kwargs: Additional parameters (temperature, max_tokens etc.)
            
        Returns:
            Response content as string
            
        Raises:
            Exception if API call fails
        """
        pass
    
    @abstractmethod
    def stream_completion(self, messages: List[Dict[str, str]], 
                         system_prompt: Optional[str] = None,
                         **kwargs) -> Generator[str, None, None]:
        """
        Stream chat completion response
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt to prepend
            **kwargs: Additional parameters
            
        Yields:
            Response chunks as strings
        """
        pass
    
    @abstractmethod
    def validate_connection(self) -> bool:
        """
        Test if API key and connection work
        
        Returns:
            True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Return list of available models for this provider
        
        Returns:
            List of model identifiers
        """
        pass
    
    def format_messages(self, messages: List[Dict[str, str]], 
                       system_prompt: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Helper to format messages with optional system prompt
        
        Args:
            messages: User/assistant messages
            system_prompt: Optional system prompt
            
        Returns:
            Formatted messages list
        """
        formatted = []
        
        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})
        
        formatted.extend(messages)
        
        return formatted
