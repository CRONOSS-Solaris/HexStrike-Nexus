"""
Modern Chat Widget with AI integration and conversation support
"""
import os
try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser,
                                 QLineEdit, QPushButton, QComboBox, QLabel, QFrame)
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtGui import QIcon
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
from ..core.config import Config
from ...i18n.manager import i18n


class ChatWidget(QWidget):
    """Modern chat widget with AI integration"""
    
    def __init__(self, ai_client: AIClient, conversation_manager: ConversationManager):
        super().__init__()
        self.setObjectName("ChatWidget")
        self.ai_client = ai_client
        self.conversation_manager = conversation_manager
        self.current_conversation_id: Optional[str] = None
        self.is_ai_thinking = False
        
        self.html_content = ""
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Header ---
        header = QFrame()
        header.setStyleSheet(f"background-color: {HexStyle.BG_SECONDARY}; border-bottom: 1px solid {HexStyle.BORDER_LIGHT};")
        header.setFixedHeight(50)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 0, 15, 0)

        self.title_label = QLabel("Select a conversation")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: 500;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()

        self.agent_combo = QComboBox()
        self.agent_combo.setMinimumWidth(180)
        self.agent_combo.addItems(['General', 'Bug Bounty', 'CTF', 'CVE Intelligence', 'Exploit Dev'])
        self.agent_combo.setVisible(False)
        header_layout.addWidget(self.agent_combo)

        layout.addWidget(header)

        # --- Chat Display ---
        if HAS_WEBENGINE:
            self.chat_display = QWebEngineView()
            self.chat_display.page().setBackgroundColor(Qt.GlobalColor.transparent)
        else:
            self.chat_display = QTextBrowser()
            self.chat_display.setOpenExternalLinks(True)
        self.chat_display.setStyleSheet("background-color: transparent;")

        layout.addWidget(self.chat_display)

        # --- Input Area ---
        input_container = QFrame()
        input_container.setStyleSheet(f"background-color: {HexStyle.BG_SECONDARY}; border-top: 1px solid {HexStyle.BORDER_LIGHT};")
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(15, 10, 15, 10)
        input_layout.setSpacing(8)
        
        # Model selector row - above message input
        model_row = QHBoxLayout()
        model_row.setSpacing(10)
        
        model_label = QLabel("Model:")
        model_label.setStyleSheet(f"color: {HexStyle.TEXT_SECONDARY}; font-size: 13px;")
        model_row.addWidget(model_label)
        
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(250)
        self.model_combo.setVisible(False)
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        model_row.addWidget(self.model_combo)
        
        model_row.addStretch()
        input_layout.addLayout(model_row)
        
        # Message input row
        message_row = QHBoxLayout()
        message_row.setSpacing(10)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(i18n.get("chat_placeholder", default="Type your message..."))
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setMinimumHeight(40)
        message_row.addWidget(self.input_field)

        self.send_btn = QPushButton(QIcon(os.path.join(Config.ICONS_DIR, "play-circle.svg")), "")
        self.send_btn.setObjectName("IconButton")
        self.send_btn.setToolTip("Send message")
        self.send_btn.clicked.connect(self.send_message)
        message_row.addWidget(self.send_btn)

        self.stop_btn = QPushButton(QIcon(os.path.join(Config.ICONS_DIR, "stop-circle.svg")), "")
        self.stop_btn.setObjectName("IconButton")
        self.stop_btn.clicked.connect(self.stop_ai_process)
        self.stop_btn.setVisible(False)
        message_row.addWidget(self.stop_btn)
        
        input_layout.addLayout(message_row)

        layout.addWidget(input_container)
        
        self.update_ai_status()
        
    def load_conversation(self, conversation_id: str):
        """Load conversation and display history"""
        self.current_conversation_id = conversation_id
        
        conv_info = self.conversation_manager.get_conversation_info(conversation_id)
        if conv_info:
            self.title_label.setText(f"{conv_info.get('title', 'Untitled')}")
            agent = conv_info.get('agent_type', 'General')
            self.agent_combo.setCurrentText(agent)
            self.agent_combo.setVisible(True)

        self.html_content = HexStyle.CHAT_HTML_TEMPLATE
        
        messages = self.conversation_manager.get_conversation_history(conversation_id)
        for msg in messages:
            self.display_message(msg['role'], msg['content'], save_to_db=False, scroll_to_bottom=False)
        
        self._update_chat_display(scroll_to_bottom=True)
        
        provider_info = self.ai_client.get_current_provider_info()
        is_enabled = provider_info is not None
        self.input_field.setEnabled(is_enabled)
        self.send_btn.setEnabled(is_enabled)
        
        if not is_enabled:
            self.input_field.setPlaceholderText("⚠️ Configure AI provider in Settings first")
    
    def send_message(self):
        """Send user message and get AI response"""
        if not self.current_conversation_id or self.is_ai_thinking:
            return
        
        user_text = self.input_field.text().strip()
        if not user_text:
            return
        
        self.input_field.clear()
        self.display_message("user", user_text)
        
        self.set_thinking_state(True)
        
        try:
            response = self.ai_client.send_message(
                self.current_conversation_id,
                user_text,
                stream=False
            )
            self.display_message("assistant", response)
        except Exception as e:
            self.display_message("system", f"Error: {str(e)}")
        finally:
            self.set_thinking_state(False)
    
    def stop_ai_process(self):
        """Stops the AI generation process."""
        # In a real streaming scenario, this would cancel the request.
        # For now, it just resets the UI state.
        self.set_thinking_state(False)

    def set_thinking_state(self, is_thinking: bool):
        """Manage UI state when AI is thinking."""
        self.is_ai_thinking = is_thinking
        self.input_field.setEnabled(not is_thinking)
        self.send_btn.setVisible(not is_thinking)
        self.stop_btn.setVisible(is_thinking)
        
        if is_thinking:
            self.display_message("typing", "")
        else:
            self._remove_typing_indicator()

        self.input_field.setFocus()

    def display_message(self, role: str, content: str, save_to_db: bool = True, scroll_to_bottom: bool = True):
        """Display a message in the chat."""
        if role == "assistant":
            content = markdown.markdown(content, extensions=['fenced_code', 'tables'])
        else:
            content = html.escape(content).replace('\n', '<br>')
        
        message_html = HexStyle.get_message_html(role, content)
        self.html_content += message_html
        
        self._update_chat_display(scroll_to_bottom)

    def _update_chat_display(self, scroll_to_bottom: bool = True):
        """Update the chat display with current HTML content."""
        full_html = self.html_content + "</body></html>"
        if HAS_WEBENGINE:
            self.chat_display.setHtml(full_html)
            if scroll_to_bottom:
                QTimer.singleShot(100, lambda: self.chat_display.page().runJavaScript("window.scrollTo(0, document.body.scrollHeight);"))
        else:
            self.chat_display.setHtml(full_html)
            if scroll_to_bottom:
                scrollbar = self.chat_display.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())

    def _remove_typing_indicator(self):
        """Remove the typing indicator from the display."""
        indicator_str = "<div class='message-container ai-container' id='typing-indicator'>"
        last_div_start = self.html_content.rfind(indicator_str)
        if last_div_start != -1:
            self.html_content = self.html_content[:last_div_start]
            self._update_chat_display()
    
    def on_model_changed(self, model_name: str):
        """Handle model selection change"""
        if not model_name or not self.current_conversation_id:
            return
        
        provider_info = self.ai_client.get_current_provider_info()
        if not provider_info:
            return
        
        db_config = self.ai_client.db.get_active_ai_provider()
        if db_config:
            self.ai_client.set_provider(
                provider_info['name'],
                db_config['api_key'],
                model_name
            )
    
    def update_ai_status(self, provider_name: str = None, model: str = None):
        """Update AI provider status and model selector"""
        provider_info = self.ai_client.get_current_provider_info()
        
        if provider_info:
            provider_name = provider_name or provider_info['name']
            model = model or provider_info.get('model', 'unknown')
            
            # Make model combo editable so user can type any model
            self.model_combo.setEditable(True)
            self.model_combo.setPlaceholderText("Enter or select model...")
            
            self.model_combo.blockSignals(True)
            self.model_combo.clear()
            
            # Only show the current model, user can edit to change
            if model:
                self.model_combo.addItem(model)
                self.model_combo.setCurrentIndex(0)
            
            self.model_combo.setVisible(True)
            self.model_combo.blockSignals(False)
            
            if self.current_conversation_id:
                self.input_field.setEnabled(True)
                self.send_btn.setEnabled(True)
                self.input_field.setPlaceholderText(i18n.get("chat_placeholder", default="Type your message..."))
        else:
            self.model_combo.setVisible(False)
            self.agent_combo.setVisible(False)
            self.input_field.setEnabled(False)
            self.send_btn.setEnabled(False)
            self.input_field.setPlaceholderText("Configure AI provider in Settings")
