"""
Modern Chat Widget with AI integration and conversation support
"""
try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser,
                                 QLineEdit, QPushButton, QComboBox, QLabel, QFrame)
    from PyQt6.QtCore import Qt, QTimer
    try:
        from PyQt6.QtWebEngineWidgets import QWebEngineView
        HAS_WEBENGINE = True
    except ImportError:
        HAS_WEBENGINE = False
except ImportError:
    HAS_WEBENGINE = False

import html
import markdown
from typing import Optional
from .styles import HexStyle
from ..core.ai_client import AIClient
from ..core.conversation_manager import ConversationManager
from ...i18n.manager import i18n


class ChatWidget(QWidget):
    """Modern chat widget with AI integration"""
    
    def __init__(self, ai_client: AIClient, conversation_manager: ConversationManager):
        super().__init__()
        self.setObjectName("ChatWidget")
        self.ai_client = ai_client
        self.conversation_manager = conversation_manager
        self.current_conversation_id: Optional[str] = None
        
        # HTML content buffer
        self.html_content = HexStyle.CHAT_HTML_TEMPLATE
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Header ---
        header = QFrame()
        header.setStyleSheet(f"background-color: {HexStyle.BG_SECONDARY}; border-bottom: 1px solid {HexStyle.BORDER_LIGHT};")
        header.setFixedHeight(65)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        # Conversation title
        self.title_label = QLabel("Select a conversation")
        self.title_label.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {HexStyle.TEXT_PRIMARY};")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        # AI Provider status
        self.ai_status_label = QLabel("⚪ No AI")
        self.ai_status_label.setStyleSheet(f"color: {HexStyle.TEXT_SECONDARY}; font-size: 12px;")
        header_layout.addWidget(self.ai_status_label)
        
        # Server Status
        self.server_status_label = QLabel(i18n.get('server_status_off', default='Server: Offline'))
        self.server_status_label.setStyleSheet(f"color: {HexStyle.STATUS_ERROR}; font-weight: bold; margin-left: 15px;")
        header_layout.addWidget(self.server_status_label)

        layout.addWidget(header)

        # --- Chat Display Area ---
        if HAS_WEBENGINE:
            self.chat_display = QWebEngineView()
            self.chat_display.setStyleSheet(f"background-color: {HexStyle.BG_MAIN};")
            self.chat_display.setHtml(self.html_content + "</body></html>")
        else:
            self.chat_display = QTextBrowser()
            self.chat_display.setOpenExternalLinks(True)
            self.chat_display.setStyleSheet(f"background-color: {HexStyle.BG_MAIN}; border: none; padding: 20px;")

        layout.addWidget(self.chat_display)

        # --- Input Area ---
        input_container = QFrame()
        input_container.setStyleSheet(
            f"background-color: {HexStyle.BG_SECONDARY}; "
            f"border-top: 1px solid {HexStyle.BORDER_LIGHT};"
        )
        input_container.setFixedHeight(90)
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(20, 15, 20, 15)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(i18n.get("chat_placeholder", default="Type your message..."))
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setMinimumHeight(50)
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Send ➜")
        self.send_btn.setFixedSize(100, 50)
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        layout.addWidget(input_container)
        
        # Update AI status
        self.update_ai_status()
        
    def load_conversation(self, conversation_id: str):
        """Load conversation and display history"""
        self.current_conversation_id = conversation_id
        
        # Get conversation info
        conv_info = self.conversation_manager.get_conversation_info(conversation_id)
        if conv_info:
            self.title_label.setText(f"💬 {conv_info.get('title', 'Untitled')}")
        
        # Clear display and reload HTML template
        self.html_content = HexStyle.CHAT_HTML_TEMPLATE
        
        # Load message history
        messages = self.conversation_manager.get_conversation_history(conversation_id)
        
        for msg in messages:
            role = msg['role']
            content = msg['content']
            self.display_message(role, content, save_to_db=False)
        
        # Update display
        self._update_chat_display()
        
        # Enable input if AI is configured
        provider_info = self.ai_client.get_current_provider_info()
        self.input_field.setEnabled(provider_info is not None)
        self.send_btn.setEnabled(provider_info is not None)
        
        if not provider_info:
            self.input_field.setPlaceholderText("⚠️ Configure AI provider in Settings first")
    
    def send_message(self):
        """Send user message and get AI response"""
        if not self.current_conversation_id:
            return
        
        user_text = self.input_field.text().strip()
        if not user_text:
            return
        
        # Disable input while processing
        self.input_field.setEnabled(False)
        self.send_btn.setEnabled(False)
        self.input_field.clear()
        
        # Display user message
        self.display_message("user", user_text, save_to_db=False)
        
        # Show thinking indicator
        thinking_msg = self.display_message("system", "🤔 AI is thinking...", save_to_db=False)
        
        try:
            # Get AI response (this also saves to DB)
            response = self.ai_client.send_message(
                self.current_conversation_id,
                user_text,
                stream=False  # TODO: Implement streaming UI
            )
            
            # Remove thinking indicator
            self._remove_last_message()
            
            # Display AI response (already marked down formatted from AI)
            self.display_message("assistant", response, save_to_db=False)
            
        except Exception as e:
            # Remove thinking indicator
            self._remove_last_message()
            
            # Show error
            error_msg = f"⚠️ Error: {str(e)}"
            self.display_message("system", error_msg, save_to_db=False)
        
        finally:
            # Re-enable input
            self.input_field.setEnabled(True)
            self.send_btn.setEnabled(True)
            self.input_field.setFocus()
    
    def display_message(self, role: str, content: str, save_to_db: bool = True):
        """
        Display message in chat
        
        Args:
            role: 'user', 'assistant', or 'system'
            content: Message content
            save_to_db: Whether to save to database (False wenn loading history)
        """
        # Process markdown for AI messages
        if role == "assistant":
            # Convert markdown to HTML
            try:
                content_html = markdown.markdown(
                    content,
                    extensions=['fenced_code', 'tables', 'nl2br']
                )
            except:
                content_html = content.replace('\n', '<br>')
        else:
            # Escape HTML for user/system messages
            content_html = html.escape(content).replace('\n', '<br>')
        
        # Generate HTML for message
        message_html = HexStyle.get_message_html(role, content_html)
        self.html_content += message_html
        
        # Update display
        self._update_chat_display()
    
    def _update_chat_display(self):
        """Update chat display with current HTML content"""
        if HAS_WEBENGINE and hasattr(self.chat_display, 'setHtml'):
            full_html = self.html_content + "</body></html>"
            self.chat_display.setHtml(full_html)
            
            # Scroll to bottom
            QTimer.singleShot(100, lambda: self.chat_display.page().runJavaScript(
                "window.scrollTo(0, document.body.scrollHeight);"
            ))
        else:
            # For QTextBrowser, append HTML
            self.chat_display.setHtml(self.html_content)
            # Scroll to bottom
            scrollbar = self.chat_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def _remove_last_message(self):
        """Remove last message from display (for removing thinking indicator)"""
        # Find and remove last message container div
        last_div_start = self.html_content.rfind("<div class='message-container")
        if last_div_start != -1:
            self.html_content = self.html_content[:last_div_start]
            self._update_chat_display()
    
    def clear_chat(self):
        """Clear chat display"""
        self.html_content = HexStyle.CHAT_HTML_TEMPLATE
        self._update_chat_display()
    
    def set_server_status(self, is_online: bool):
        """Update server status indicator"""
        if is_online:
            self.server_status_label.setText(i18n.get('server_status_on', default='Server: Online'))
            self.server_status_label.setStyleSheet(f"color: {HexStyle.STATUS_SUCCESS}; font-weight: bold;")
        else:
            self.server_status_label.setText(i18n.get('server_status_off', default='Server: Offline'))
            self.server_status_label.setStyleSheet(f"color: {HexStyle.STATUS_ERROR}; font-weight: bold;")
    
    def update_ai_status(self):
        """Update AI provider status display"""
        provider_info = self.ai_client.get_current_provider_info()
        
        if provider_info:
            name = provider_info['name']
            model = provider_info.get('model', 'unknown')
            
            # Shorten model name for display
            model_short = model.split('/')[-1] if '/' in model else model
            if len(model_short) > 20:
                model_short = model_short[:17] + "..."
            
            self.ai_status_label.setText(f"🤖 {name}: {model_short}")
            self.ai_status_label.setStyleSheet(f"color: {HexStyle.STATUS_SUCCESS}; font-size: 12px; font-weight: 500;")
            
            # Enable sending if conversation is loaded
            if self.current_conversation_id:
                self.input_field.setEnabled(True)
                self.send_btn.setEnabled(True)
                self.input_field.setPlaceholderText(i18n.get("chat_placeholder", default="Type your message..."))
        else:
            self.ai_status_label.setText("⚪ No AI Provider")
            self.ai_status_label.setStyleSheet(f"color: {HexStyle.TEXT_MUTED}; font-size: 12px;")
            
            # Disable sending
            self.input_field.setEnabled(False)
            self.send_btn.setEnabled(False)
            self.input_field.setPlaceholderText("⚠️ Configure AI provider in Settings")
    
    def get_current_conversation_id(self) -> Optional[str]:
        """Get current conversation ID"""
        return self.current_conversation_id

