"""
AI Client - Main orchestrator for AI providers and HexStrike integration
"""
import json
import re
from typing import Optional, Dict, List, Generator
from .ai_providers import OpenRouterProvider, OpenAIProvider, AnthropicProvider
from .ai_provider_base import AIProviderBase
from .conversation_manager import ConversationManager
from .system_prompts import SystemPrompts
from .database import DatabaseManager
from .api_client import APIClient
from .reporter import Reporter


class AIClient:
    """Main AI client that orchestrates providers and HexStrike integration"""
    
    PROVIDER_CLASSES = {
        'openrouter': OpenRouterProvider,
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider
    }
    
    def __init__(self, db: Optional[DatabaseManager] = None):
        """
        Initialize AI client
        
        Args:
            db: Database manager instance (creates new if None)
        """
        self.db = db or DatabaseManager()
        self.conversation_manager = ConversationManager(self.db)
        self.active_provider: Optional[AIProviderBase] = None
        self.active_provider_name: str = ""
        
        # Try to load active provider from database
        self._load_active_provider()
    
    def _load_active_provider(self):
        """Load active AI provider from database"""
        config = self.db.get_active_ai_provider()
        if config:
            self.set_provider(
                config['name'],
                config['api_key'],
                config['model'],
                config.get('config', {})
            )
    
    def set_provider(self, provider_name: str, api_key: str, model: str, 
                    config: Dict = None) -> bool:
        """
        Configure and set active AI provider
        
        Args:
            provider_name: Provider identifier ('openrouter', 'openai', 'anthropic')
            api_key: API key for the provider
            model: Model identifier
            config: Additional configuration
            
        Returns:
            True if provider set successfully
        """
        if provider_name not in self.PROVIDER_CLASSES:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        provider_class = self.PROVIDER_CLASSES[provider_name]
        config = config or {}
        
        try:
            self.active_provider = provider_class(api_key, model, **config)
            self.active_provider_name = provider_name
            
            # Save to database as active provider
            self.db.save_ai_provider_config(
                provider_name, api_key, model, 
                is_active=True, config=config
            )
            
            return True
        except Exception as e:
            print(f"Error setting provider: {e}")
            return False
    
    def test_connection(self) -> tuple[bool, str]:
        """
        Test current provider connection
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.active_provider:
            return False, "No AI provider configured"
        
        try:
            if self.active_provider.validate_connection():
                return True, f"Connection to {self.active_provider_name} successful!"
            else:
                return False, "Connection failed - check API key"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def send_message(self, conversation_id: str, message: str, 
                    stream: bool = False) -> str:
        """
        Send message in context of conversation
        
        Args:
            conversation_id: ID of conversation
            message: User message
            stream: Whether to stream response
            
        Returns:
            AI response (or generator if streaming)
        """
        if not self.active_provider:
            return "⚠️ No AI provider configured. Please configure an AI provider in Settings."
        
        # Get conversation info for agent type
        conv_info = self.conversation_manager.get_conversation_info(conversation_id)
        if not conv_info:
            return "⚠️ Conversation not found"
        
        agent_type = conv_info.get('agent_type', 'General')
        
        # Add user message to conversation
        self.conversation_manager.add_message(
            conversation_id, 
            'user', 
            message
        )
        
        # Get conversation history
        history = self.conversation_manager.format_messages_for_api(
            conversation_id,
            limit=50  # Last 50 messages for context
        )
        
        # Get appropriate system prompt
        system_prompt = SystemPrompts.get_prompt_for_agent(agent_type)
        
        try:
            if stream:
                return self._stream_and_save_response(
                    conversation_id, history, system_prompt
                )
            else:
                # Get response from AI
                response = self.active_provider.chat_completion(
                    history, 
                    system_prompt=system_prompt
                )
                
                # Parse for HexStrike actions
                response_with_actions = self._process_hexstrike_actions(response)
                
                # Save assistant message
                self.conversation_manager.add_message(
                    conversation_id,
                    'assistant',
                    response_with_actions,
                    metadata={'model': self.active_provider.model}
                )
                
                return response_with_actions
                
        except Exception as e:
            error_msg = f"⚠️ AI Error: {str(e)}"
            # Save error as system message
            self.conversation_manager.add_message(
                conversation_id,
                'system',
                error_msg
            )
            return error_msg
    
    def _stream_and_save_response(self, conversation_id: str, 
                                  history: List[Dict], 
                                  system_prompt: str) -> Generator:
        """
        Stream response and save when complete
        
        Args:
            conversation_id: Conversation ID
            history: Message history
            system_prompt: System prompt
            
        Yields:
            Response chunks
        """
        full_response = ""
        
        try:
            for chunk in self.active_provider.stream_completion(history, system_prompt):
                full_response += chunk
                yield chunk
            
            # Process HexStrike actions after streaming complete
            processed_response = self._process_hexstrike_actions(full_response)
            
            # If actions were executed, yield the action results
            if processed_response != full_response:
                action_results = processed_response[len(full_response):]
                yield action_results
            
            # Save complete response
            self.conversation_manager.add_message(
                conversation_id,
                'assistant',
                processed_response,
                metadata={'model': self.active_provider.model, 'streamed': True}
            )
            
        except Exception as e:
            error_msg = f"\n\n⚠️ Error: {str(e)}"
            yield error_msg
            
            self.conversation_manager.add_message(
                conversation_id,
                'system',
                f"Stream error: {str(e)}"
            )
    
    def _process_hexstrike_actions(self, response: str) -> str:
        """
        Parse AI response for HexStrike actions and execute them
        
        Args:
            response: AI response text
            
        Returns:
            Response with action results appended
        """
        # Look for hexstrike action blocks
        pattern = r'```hexstrike\s*\n(.*?)\n```'
        matches = re.findall(pattern, response, re.DOTALL)
        
        if not matches:
            return response
        
        action_results = "\n\n---\n**🔧 HexStrike Execution:**\n"
        
        for match in matches:
            try:
                action_data = json.loads(match)
                result = self._execute_hexstrike_action(action_data)
                action_results += f"\n{result}\n"
            except json.JSONDecodeError:
                action_results += "\n⚠️ Invalid action format\n"
            except Exception as e:
                action_results += f"\n⚠️ Action failed: {str(e)}\n"
        
        return response + action_results
   
    def _execute_hexstrike_action(self, action: Dict) -> str:
        """
        Execute HexStrike command based on AI decision
        
        Args:
            action: Action dictionary with agent, target, action type
            
        Returns:
            Execution result message
        """
        agent = action.get('agent')
        target = action.get('target')
        action_type = action.get('action', 'analyze')
        
        if not target:
            return "⚠️ No target specified"
        
        result_msg = f"🎯 Target: **{target}**\n"
        result_msg += f"🤖 Agent: **{agent}**\n"
        result_msg += f"⚡ Action: **{action_type}**\n\n"
        
        # Execute based on action type
        if action_type == 'full_recon' or action_type == 'analyze':
            # 1. Select tools
            tools_resp = APIClient.select_tools(target)
            tools = tools_resp.get("tools", []) if tools_resp else []
            
            result_msg += "**Tools Selected:**\n"
            for tool in tools:
                result_msg += f"- `{tool}`\n"
            
            # 2. Analyze target
            analysis = APIClient.analyze_target(target)
            plan = analysis.get("plan", []) if analysis else []
            
            result_msg += "\n**Execution Plan:**\n"
            for step in plan:
                result_msg += f"- {step}\n"
            
            # 3. Generate report
            try:
                report_path = Reporter.generate_report(target, plan, "pl")
                result_msg += f"\n✅ **Report generated:** `{report_path}`"
            except Exception as e:
                result_msg += f"\n⚠️ Report generation failed: {str(e)}"
                
        elif action_type == 'scan':
            # Quick scan
            tools_resp = APIClient.select_tools(target)
            tools = tools_resp.get("tools", []) if tools_resp else []
            
            result_msg += "**Scanning with:**\n"
            for tool in tools[:3]:  # Limit to top 3 tools for quick scan
                result_msg += f"- `{tool}`\n"
            
            result_msg += "\n🔄 Scan in progress... (check Telemetry for real-time status)"
            
        else:
            result_msg += f"⚠️ Unknown action type: {action_type}"
        
        return result_msg
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return list(self.PROVIDER_CLASSES.keys())
    
    def get_current_provider_info(self) -> Optional[Dict]:
        """Get current provider information"""
        if not self.active_provider:
            return None
        
        return {
            'name': self.active_provider_name,
            'model': self.active_provider.model
        }
    
    # Legacy method for backward compatibility
    def process_user_request(self, user_input: str, selected_agent: str, language: str = "pl") -> str:
        """
        Legacy method - creates temporary conversation
        
        DEPRECATED: Use send_message with proper conversation management instead
        """
        # Create temporary conversation
        conv_id = self.conversation_manager.create_conversation(
            "Legacy Chat",
            selected_agent
        )
        
        # Send message
        response = self.send_message(conv_id, user_input)
        
        return response

