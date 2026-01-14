"""
Modern Main Window with three-panel layout
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QStackedWidget, QSplitter, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon

from .conversation_sidebar import ConversationSidebar
from .chat_widget import ChatWidget
from .ai_provider_widget import AIProviderWidget
from .telemetry_widget import TelemetryWidget
from .settings_widget import SettingsWidget
from .styles import HexStyle
from ..core.api_client import APIClient
from ..core.config import Config
from ..core.database import DatabaseManager
from ..core.ai_client import AIClient
from ..core.conversation_manager import ConversationManager
from ...i18n.manager import i18n


class MainWindow(QMainWindow):
    """Modern main window with conversation-based chat"""
    
    def __init__(self, server_manager):
        super().__init__()
        
        # Load language from config
        i18n.load_language(Config.LANGUAGE)
        
        self.server_manager = server_manager
        self.setWindowTitle(f"HexStrike Nexus v{Config.VERSION}")
        self.resize(1400, 900)
        
        # Initialize core components
        self.db = DatabaseManager()
        self.ai_client = AIClient(self.db)
        self.conversation_manager = ConversationManager(self.db)
        
        # Apply Global Styles
        self.setStyleSheet(HexStyle.APP_STYLE)
        
        self.init_ui()
        
        # Setup update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)  # Every 2 seconds
        
        # Check if AI is configured, if not show prompt
        QTimer.singleShot(500, self.check_ai_configuration)
    
    def init_ui(self):
        """Initialize UI with modern three-panel layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        # Create main content splitter (conversations | chat)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setHandleWidth(1)
        self.main_splitter.setStyleSheet(f"QSplitter::handle {{ background: {HexStyle.BORDER_LIGHT}; }}")
        
        # === LEFT PANEL: Conversation Sidebar ===
        self.conversation_sidebar = ConversationSidebar(self.conversation_manager)
        self.conversation_sidebar.conversation_selected.connect(self.on_conversation_selected)
        self.conversation_sidebar.conversation_deleted.connect(self.on_conversation_deleted)
        self.conversation_sidebar.setMinimumWidth(280)
        self.conversation_sidebar.setMaximumWidth(400)
        self.main_splitter.addWidget(self.conversation_sidebar)
        
        # === MIDDLE PANEL: Stacked Widget for Main Content ===
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("ContentArea")
        
        # Chat Widget
        self.chat_widget = ChatWidget(self.ai_client, self.conversation_manager)
        self.content_stack.addWidget(self.chat_widget)  # Index 0
        
        # Telemetry Widget
        self.telemetry_widget = TelemetryWidget()
        self.content_stack.addWidget(self.telemetry_widget)  # Index 1
        
        # Settings Stack (with AI Provider config)
        settings_container = QWidget()
        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        
        self.settings_widget = SettingsWidget()
        self.ai_provider_widget = AIProviderWidget(self.ai_client)
        self.ai_provider_widget.provider_configured.connect(self.on_provider_configured)
        
        # Create tabbed interface for settings
        from PyQt6.QtWidgets import QTabWidget
        settings_tabs = QTabWidget()
        settings_tabs.addTab(self.ai_provider_widget, "🤖 AI Provider")
        settings_tabs.addTab(self.settings_widget, "⚙️ General")
        
        settings_layout.addWidget(settings_tabs)
        self.content_stack.addWidget(settings_container)  # Index 2
        
        self.main_splitter.addWidget(self.content_stack)
        
        # Set splitter sizes (conversations 25%, content 75%)
        self.main_splitter.setSizes([350, 1050])
        
        main_layout.addWidget(self.main_splitter)
        
        # Check if we have conversations, if not create a welcome one
        convs = self.conversation_manager.get_all_conversations()
        if not convs:
            self.create_welcome_conversation()
        else:
            # Select first conversation
            first_conv = convs[0]
            self.conversation_sidebar.set_current_conversation(first_conv['id'])
            self.chat_widget.load_conversation(first_conv['id'])
    
    def create_welcome_conversation(self):
        """Create initial welcome conversation"""
        conv_id = self.conversation_manager.create_conversation(
            "Welcome to HexStrike Nexus",
            "General"
        )
        
        # Add welcome message
        welcome_msg = """# Welcome to HexStrike Nexus! 🎯

**Your Advanced Cybersecurity AI Assistant**

I'm powered by cutting-edge AI and the HexStrike framework with 150+ security tools.

## Getting Started

1. **Configure AI Provider** - Go to Settings → AI Provider tab to set up your API key
2. **Choose Your Agent** - Each conversation can use different specialized agents:
   - 🎯 **Bug Bounty** - Web application security testing
   - 🏴 **CTF** - Capture The Flag challenges
   - 🐛 **CVE Intelligence** - Vulnerability research
   - 💣 **Exploit Dev** - Exploit development

3. **Start Chatting** - Ask me to analyze targets, scan for vulnerabilities, or help with security tasks!

## Example Commands

- "Scan example.com for vulnerabilities"
- "Help me solve this CTF challenge"
- "Find CVEs for Apache 2.4.49"
- "Generate exploit for CVE-2021-xxxxx"

**Note:** Always ensure you have proper authorization before testing any targets.

Ready to begin? Configure your AI provider in Settings! 🚀
"""
        
        self.conversation_manager.add_message(conv_id, "assistant", welcome_msg)
        
        # Refresh sidebar and select this conversation
        self.conversation_sidebar.refresh_conversations()
        self.conversation_sidebar.set_current_conversation(conv_id)
        self.chat_widget.load_conversation(conv_id)
    
    def on_conversation_selected(self, conversation_id: str):
        """Handle conversation selection"""
       # Switch to chat view
        self.content_stack.setCurrentIndex(0)
        
        # Load conversation in chat widget
        self.chat_widget.load_conversation(conversation_id)
    
    def on_conversation_deleted(self, conversation_id: str):
        """Handle conversation deletion"""
        # If deleted conversation was active, show first available or create new
        convs = self.conversation_manager.get_all_conversations()
        if convs:
            first_conv = convs[0]
            self.chat_widget.load_conversation(first_conv['id'])
        else:
            self.create_welcome_conversation()
    
    def check_ai_configuration(self):
        """Check if AI is configured, prompt user if not"""
        provider_info = self.ai_client.get_current_provider_info()
        
        if not provider_info:
            reply = QMessageBox.question(
                self,
                "AI Provider Not Configured",
                "No AI provider is configured. Would you like to configure one now?\n\n"
                "You need an API key from OpenRouter, OpenAI, or Anthropic to use AI features.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Show settings with AI provider tab
                self.content_stack.setCurrentIndex(2)
    
    def on_provider_configured(self, provider_name: str, model: str):
        """Handle successful provider configuration"""
        # Update chat widget AI status
        self.chat_widget.update_ai_status()
        
        # Show success message
        QMessageBox.information(
            self,
            "Success!",
            f"AI Provider '{provider_name}' configured successfully!\n\n"
            f"You can now use AI features in your conversations."
        )
        
        # Switch back to chat
        self.content_stack.setCurrentIndex(0)
    
    def display_page(self, index: int):
        """Display specific page (for menu/shortcuts)"""
        self.content_stack.setCurrentIndex(index)
    
    def update_status(self):
        """Update status indicators"""
        # Update server status
        if self.server_manager.is_running():
            self.chat_widget.set_server_status(True)
            
            # Only update telemetry if visible
            if self.content_stack.currentIndex() == 1:
                self.update_telemetry()
        else:
            self.chat_widget.set_server_status(False)
    
    def update_telemetry(self):
        """Update telemetry data"""
        try:
            data = APIClient.get_telemetry()
            if data:
                self.telemetry_widget.update_data(data)
            
            logs = APIClient.get_logs()
            if logs:
                self.telemetry_widget.update_logs(logs)
            
            cache_stats = APIClient.get_cache_stats()
            if cache_stats:
                self.telemetry_widget.update_cache_stats(cache_stats)
        except Exception as e:
            pass  # Silently fail telemetry updates
    
    def closeEvent(self, event):
        """Handle window close"""
        # Stop server
        self.server_manager.stop_server()
        event.accept()

