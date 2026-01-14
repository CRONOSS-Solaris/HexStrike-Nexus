"""
Conversation Manager for handling multiple chat sessions
"""
from typing import List, Dict, Optional
from .database import DatabaseManager


class ConversationManager:
    """Manages conversations and message history"""
    
    def __init__(self, db: DatabaseManager):
        """
        Initialize conversation manager
        
        Args:
            db: Database manager instance
        """
        self.db = db
        
    def create_conversation(self, title: str = "New Chat", 
                          agent_type: str = "BugBountyWorkflowManager") -> str:
        """
        Create new conversation
        
        Args:
            title: Conversation title
            agent_type: Type of agent for this conversation
            
        Returns:
            Conversation ID
        """
        return self.db.create_conversation(title, agent_type)
    
    def get_all_conversations(self, archived: bool = False) -> List[Dict]:
        """
        Get all conversations
        
        Args:
            archived: Whether to get archived conversations
            
        Returns:
            List of conversation metadata dicts
        """
        return self.db.get_all_conversations(archived)
    
    def get_conversation_history(self, conversation_id: str, 
                                limit: int = 100) -> List[Dict]:
        """
        Get message history for conversation
        
        Args:
            conversation_id: ID of conversation
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dicts with role, content, timestamp
        """
        return self.db.get_conversation_messages(conversation_id, limit)
    
    def add_message(self, conversation_id: str, role: str, content: str,
                   metadata: Optional[Dict] = None):
        """
        Add message to conversation
        
        Args:
            conversation_id: ID of conversation
            role: Message role ('user', 'assistant', 'system')
            content: Message content
            metadata: Optional metadata (model used, tokens, etc.)
        """
        self.db.add_message_to_conversation(conversation_id, role, content, metadata)
    
    def update_conversation_title(self, conversation_id: str, title: str):
        """
        Update conversation title
        
        Args:
            conversation_id: ID of conversation
            title: New title
        """
        self.db.update_conversation_title(conversation_id, title)
    
    def delete_conversation(self, conversation_id: str):
        """
        Delete conversation and all messages
        
        Args:
            conversation_id: ID of conversation to delete
        """
        self.db.delete_conversation(conversation_id)
    
    def archive_conversation(self, conversation_id: str, archived: bool = True):
        """
        Archive or unarchive conversation
        
        Args:
            conversation_id: ID of conversation
            archived: Whether to archive or unarchive
        """
        self.db.archive_conversation(conversation_id, archived)
    
    def format_messages_for_api(self, conversation_id: str, 
                               limit: int = 50) -> List[Dict[str, str]]:
        """
        Format conversation history for AI API
        
        Args:
            conversation_id: ID of conversation
            limit: Maximum number of messages
            
        Returns:
            List of messages in API format
        """
        messages = self.get_conversation_history(conversation_id, limit)
        
        # Convert to simple format for API
        api_messages = []
        for msg in messages:
            api_messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        return api_messages
    
    def get_conversation_info(self, conversation_id: str) -> Optional[Dict]:
        """
        Get conversation metadata
        
        Args:
            conversation_id: ID of conversation
            
        Returns:
            Conversation info dict or None if not found
        """
        convs = self.db.get_all_conversations()
        for conv in convs:
            if conv['id'] == conversation_id:
                return conv
        return None
