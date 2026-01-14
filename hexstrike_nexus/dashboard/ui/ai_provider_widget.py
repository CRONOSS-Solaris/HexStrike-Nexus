"""
AI Provider Configuration Widget
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QGroupBox,
                             QFormLayout, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from .styles import HexStyle
from ..core.ai_client import AIClient
from ..core.database import DatabaseManager


class AIProviderWidget(QWidget):
    """Widget for configuring AI providers"""
    
    # Signal emitted when provider is successfully configured
    provider_configured = pyqtSignal(str, str)  # provider_name, model
    
    def __init__(self, ai_client: AIClient):
        super().__init__()
        self.ai_client = ai_client
        self.init_ui()
        self.load_current_config()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # Title
        title = QLabel("AI Provider Configuration")
        title.setObjectName("HeaderTitle")
        layout.addWidget(title)
        
        # Info message
        info_label = QLabel(
            "Configure your AI provider to enable intelligent features. "
            "You need to provide your own API key."
        )
        info_label.setObjectName("SubTitle")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Configuration Group
        config_group = QGroupBox("Provider Settings")
        config_layout = QFormLayout()
        config_layout.setSpacing(15)
        config_group.setLayout(config_layout)
        
        # Provider selection
        self.provider_combo = QComboBox()
        providers = self.ai_client.get_available_providers()
        self.provider_combo.addItems(providers)
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        config_layout.addRow("Provider:", self.provider_combo)
        
        # API Key input
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("sk-...")
        config_layout.addRow("API Key:", self.api_key_input)
        
        # Show/Hide API key toggle
        api_key_layout = QHBoxLayout()
        self.show_key_btn = QPushButton("Show")
        self.show_key_btn.setObjectName("SecondaryButton")
        self.show_key_btn.setMaximumWidth(80)
        self.show_key_btn.clicked.connect(self.toggle_api_key_visibility)
        api_key_layout.addWidget(self.api_key_input)
        api_key_layout.addWidget(self.show_key_btn)
        config_layout.addRow("API Key:", api_key_layout)
        
        # Model selection
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.setPlaceholderText("Select or enter model name...")
        config_layout.addRow("Model:", self.model_combo)
        
        layout.addWidget(config_group)
        
        # Status display
        self.status_label = QLabel("Not configured")
        self.status_label.setObjectName("SubTitle")
        layout.addWidget(self.status_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.test_btn = QPushButton("Test Connection")
        self.test_btn.setObjectName("SecondaryButton")
        self.test_btn.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_btn)
        
        self.save_btn = QPushButton("Save & Activate")
        self.save_btn.clicked.connect(self.save_configuration)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        # Help section
        help_group = QGroupBox("Getting API Keys")
        help_layout = QVBoxLayout()
        help_group.setLayout(help_layout)
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setMaximumHeight(150)
        help_text.setHtml(f"""
        <style>
            body {{ color: {HexStyle.TEXT_SECONDARY}; font-size: 13px; }}
            a {{ color: {HexStyle.ACCENT_SECONDARY}; }}
        </style>
        <p><b>OpenRouter:</b> <a href="https://openrouter.ai/keys">https://openrouter.ai/keys</a><br/>
        Access to multiple models (Claude, GPT-4, Gemini, etc.) through one API</p>
        
        <p><b>OpenAI:</b> <a href="https://platform.openai.com/api-keys">https://platform.openai.com/api-keys</a><br/>
        GPT-4o, GPT-4 Turbo, GPT-3.5</p>
        
        <p><b>Anthropic:</b> <a href="https://console.anthropic.com/settings/keys">https://console.anthropic.com/settings/keys</a><br/>
        Claude 3.5 Sonnet, Opus, Haiku</p>
        
        <p><b>Google Gemini:</b> <a href="https://aistudio.google.com/app/apikey">https://aistudio.google.com/app/apikey</a><br/>
        Gemini 1.5 Pro, Flash, Vision</p>
        """)
        help_layout.addWidget(help_text)
        
        layout.addWidget(help_group)
        
        layout.addStretch()
        
    def on_provider_changed(self, provider_name: str):
        """Handle provider selection change"""
        # Clear model field when provider changes
        self.model_combo.clear()
        
        # Set helpful placeholder based on provider
        if provider_name == "openrouter":
            self.model_combo.setPlaceholderText("e.g., anthropic/claude-3.5-sonnet, openai/gpt-4o")
        elif provider_name == "openai":
            self.model_combo.setPlaceholderText("e.g., gpt-4o, gpt-4-turbo")
        elif provider_name == "anthropic":
            self.model_combo.setPlaceholderText("e.g., claude-3-5-sonnet-20241022")
        elif provider_name == "gemini":
            self.model_combo.setPlaceholderText("e.g., gemini-1.5-pro-latest, gemini-pro")
        else:
            self.model_combo.setPlaceholderText("Enter model name...")
    
    
    def toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_key_btn.setText("Hide")
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_key_btn.setText("Show")
    
    def test_connection(self):
        """Test AI provider connection"""
        provider_name = self.provider_combo.currentText()
        api_key = self.api_key_input.text().strip()
        model = self.model_combo.currentText().strip()
        
        if not api_key:
            QMessageBox.warning(self, "Missing API Key", "Please enter your API key.")
            return
        
        if not model:
            QMessageBox.warning(self, "Missing Model", "Please select or enter a model name.")
            return
        
        self.status_label.setText("Testing connection...")
        self.test_btn.setEnabled(False)
        
        try:
            # Try to set provider
            success = self.ai_client.set_provider(provider_name, api_key, model)
            
            if success:
                # Test connection
                test_success, message = self.ai_client.test_connection()
                
                if test_success:
                    self.status_label.setText(f"Connected: {provider_name} - {model}")
                    self.status_label.setStyleSheet(f"color: {HexStyle.STATUS_SUCCESS};")
                    QMessageBox.information(self, "Success", message)
                else:
                    self.status_label.setText(f"Failed: {message}")
                    self.status_label.setStyleSheet(f"color: {HexStyle.STATUS_ERROR};")
                    QMessageBox.warning(self, "Test Failed", message)
            else:
                self.status_label.setText("Failed to configure provider")
                self.status_label.setStyleSheet(f"color: {HexStyle.STATUS_ERROR};")
                
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.status_label.setStyleSheet(f"color: {HexStyle.STATUS_ERROR};")
            QMessageBox.critical(self, "Error", f"Failed to test connection:\n{str(e)}")
        
        finally:
            self.test_btn.setEnabled(True)
    
    def save_configuration(self):
        """Save provider configuration"""
        provider_name = self.provider_combo.currentText()
        api_key = self.api_key_input.text().strip()
        model = self.model_combo.currentText().strip()
        
        if not api_key:
            QMessageBox.warning(self, "Missing API Key", "Please enter your API key.")
            return
        
        if not model:
            QMessageBox.warning(self, "Missing Model", "Please select or enter a model name.")
            return
        
        try:
            # Set and activate provider
            success = self.ai_client.set_provider(provider_name, api_key, model)
            
            if success:
                self.status_label.setText(f"Active: {provider_name} - {model}")
                self.status_label.setStyleSheet(f"color: {HexStyle.STATUS_SUCCESS};")
                
                QMessageBox.information(
                    self,
                    "Configuration Saved",
                    f"AI Provider '{provider_name}' with model '{model}' has been configured and activated.\n\n"
                    f"You can now use AI features in your chats!"
                )
                
                # Emit signal
                self.provider_configured.emit(provider_name, model)
            else:
                QMessageBox.warning(self, "Save Failed", "Failed to save configuration.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration:\n{str(e)}")
    
    def load_current_config(self):
        """Load current provider configuration"""
        provider_info = self.ai_client.get_current_provider_info()
        
        if provider_info:
            provider_name = provider_info['name']
            model = provider_info['model']
            
            # Set provider in combo
            index = self.provider_combo.findText(provider_name)
            if index >= 0:
                self.provider_combo.setCurrentIndex(index)
            
            # Set model
            self.model_combo.setCurrentText(model)
            
            # Update status
            self.status_label.setText(f"Active: {provider_name} - {model}")
            self.status_label.setStyleSheet(f"color: {HexStyle.STATUS_SUCCESS};")
            
            # Note: We don't load the API key for security reasons
            self.api_key_input.setPlaceholderText("API key is saved (hidden for security)")
        else:
            self.status_label.setText("No provider configured")
            self.status_label.setStyleSheet(f"color: {HexStyle.TEXT_SECONDARY};")
