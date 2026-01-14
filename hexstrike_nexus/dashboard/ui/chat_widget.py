try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser,
                                 QLineEdit, QPushButton, QComboBox, QLabel, QFrame)
    from PyQt6.QtCore import Qt
    try:
        from PyQt6.QtWebEngineWidgets import QWebEngineView
        HAS_WEBENGINE = True
    except ImportError:
        HAS_WEBENGINE = False
except ImportError:
    # ... (Mocks for non-PyQt environments - omitted for brevity in replacement but kept if needed)
    HAS_WEBENGINE = False

import html
from .styles import HexStyle
from ..core.ai_client import AIClient
from ..core.database import DatabaseManager
from ...i18n.manager import i18n
from ..core.config import Config

class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ChatWidget")
        self.ai_client = AIClient()
        self.db = DatabaseManager()
        # Use stylesheet for base HTML
        self.html_content = HexStyle.CHAT_HTML_TEMPLATE
        self.init_ui()
        self.load_history()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Header ---
        header = QFrame()
        header.setStyleSheet(f"background-color: {HexStyle.BG_SIDEBAR}; border-bottom: 1px solid {HexStyle.BORDER_LIGHT};")
        header.setFixedHeight(60)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        # Title
        title = QLabel(i18n.get("agent_label"))
        title.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {HexStyle.TEXT_PRIMARY};")
        header_layout.addWidget(title)

        # Agent Selector
        self.agent_selector = QComboBox()
        self.agent_selector.addItems([
            "BugBountyWorkflowManager",
            "CTFWorkflowManager",
            "CVEIntelligenceManager",
            "AIExploitGenerator"
        ])
        self.agent_selector.setFixedWidth(200)
        header_layout.addWidget(self.agent_selector)
        
        header_layout.addStretch()
        
        # Status Label
        self.status_label = QLabel(i18n.get('server_status_off'))
        self.status_label.setStyleSheet(f"color: {HexStyle.STATUS_ERROR}; font-weight: bold;")
        header_layout.addWidget(self.status_label)

        layout.addWidget(header)

        # --- Chat Area ---
        if HAS_WEBENGINE:
            self.chat_display = QWebEngineView()
            self.chat_display.setStyleSheet(f"background-color: {HexStyle.BG_MAIN};")
        else:
            self.chat_display = QTextBrowser()
            self.chat_display.setOpenExternalLinks(True)
            self.chat_display.setStyleSheet(f"background-color: {HexStyle.BG_MAIN}; border: none;")

        layout.addWidget(self.chat_display)

        # --- Input Area ---
        input_container = QFrame()
        input_container.setStyleSheet(f"background-color: {HexStyle.BG_SIDEBAR}; border-top: 1px solid {HexStyle.BORDER_LIGHT};")
        input_container.setFixedHeight(80)
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(20, 15, 20, 15)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(i18n.get("chat_placeholder"))
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("->")
        self.send_btn.setFixedSize(50, 40)
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        layout.addWidget(input_container)

    def load_history(self):
        history = self.db.get_history(limit=20)
        if not history:
             return

        for row in history:
            role, message, agent, timestamp = row
            self.display_message(role, message)

    def set_server_status(self, is_online):
        if is_online:
            self.status_label.setText(i18n.get('server_status_on'))
            self.status_label.setStyleSheet(f"color: {HexStyle.STATUS_SUCCESS}; font-weight: bold;")
        else:
            self.status_label.setText(i18n.get('server_status_off'))
            self.status_label.setStyleSheet(f"color: {HexStyle.STATUS_ERROR}; font-weight: bold;")

    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return

        agent = self.agent_selector.currentText()
        lang = Config.LANGUAGE

        # Display and Save User Message
        self.display_message("User", user_text)
        self.db.add_message("User", user_text, agent)
        
        self.input_field.clear()

        # Process with AI
        response = self.ai_client.process_user_request(user_text, agent, language=lang)

        # Display and Save AI Message
        self.display_message("Nexus", response)
        self.db.add_message("Nexus", response, agent)

    def display_message(self, role, text):
        safe_text = text if role == "Nexus" else html.escape(text)
        
        if role == "User":
            div = f"""
            <div class='message-container user-container'>
                <div class='message-header'>Ty</div>
                <div class='message-bubble user-bubble'>{safe_text}</div>
            </div>
            """
        elif role == "Nexus":
            div = f"""
            <div class='message-container ai-container'>
                <div class='message-header'>Nexus</div>
                <div class='message-bubble ai-bubble'>{safe_text}</div>
            </div>
            """
        else:
            div = f"""
            <div class='message-container system-container'>
                <div class='message-bubble system-bubble'>{safe_text}</div>
            </div>
            """

        if HAS_WEBENGINE and hasattr(self.chat_display, 'setHtml'):
            self.html_content += div
            self.chat_display.setHtml(self.html_content + "</body></html>")
            self.chat_display.page().runJavaScript("window.scrollTo(0, document.body.scrollHeight);")
        else:
            self.chat_display.append(div)
