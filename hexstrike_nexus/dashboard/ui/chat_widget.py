try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser,
                                 QLineEdit, QPushButton, QComboBox, QLabel)
    from PyQt6.QtCore import Qt
    try:
        from PyQt6.QtWebEngineWidgets import QWebEngineView
        HAS_WEBENGINE = True
    except ImportError:
        HAS_WEBENGINE = False
except ImportError:
    class QWidget:
        def setLayout(self, l): pass
    class QVBoxLayout:
        def addWidget(self, w): pass
        def addLayout(self, l): pass
    class QHBoxLayout:
        def addWidget(self, w): pass
        def addStretch(self): pass
    class QTextBrowser:
        def append(self, t): pass
        def setHtml(self, h): pass
        def setOpenExternalLinks(self, b): pass
    class QWebEngineView:
        def setHtml(self, h): pass
        def page(self): return self
        def runJavaScript(self, s): pass
    class QLineEdit:
        def text(self): return ""
        def clear(self): pass
        def returnPressed(self): pass
        def connect(self, f): pass
    class QPushButton:
        def clicked(self): pass
    class QComboBox:
        def addItems(self, i): pass
        def currentText(self): return ""
    class QLabel:
        def setText(self, t): pass
        def setStyleSheet(self, s): pass
    class Qt:
        pass
    HAS_WEBENGINE = False

from ..core.ai_client import AIClient
from ..core.database import DatabaseManager

class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ai_client = AIClient()
        self.db = DatabaseManager()
        self.html_content = "<html><body style='font-family: sans-serif; padding: 10px;'>"
        self.init_ui()
        self.load_history()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header: Status, Agent Selector, Language
        header_layout = QHBoxLayout()

        self.status_label = QLabel("HexStrike: DISCONNECTED")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        header_layout.addWidget(self.status_label)

        header_layout.addStretch()

        # Language Selector
        header_layout.addWidget(QLabel("Język:"))
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(["Polski", "English"])
        header_layout.addWidget(self.lang_selector)

        # Agent Selector
        header_layout.addWidget(QLabel("Agent:"))
        self.agent_selector = QComboBox()
        self.agent_selector.addItems([
            "BugBountyWorkflowManager",
            "CTFWorkflowManager",
            "CVEIntelligenceManager",
            "AIExploitGenerator"
        ])
        header_layout.addWidget(self.agent_selector)

        layout.addLayout(header_layout)

        # Chat Area
        if HAS_WEBENGINE:
            self.chat_display = QWebEngineView()
        else:
            self.chat_display = QTextBrowser()
            self.chat_display.setOpenExternalLinks(True)

        layout.addWidget(self.chat_display)

        # Input Area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Wpisz polecenie (np. 'Zrób recon domeny example.com')...")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Wyślij")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        layout.addLayout(input_layout)

    def load_history(self):
        history = self.db.get_history(limit=20)
        # History rows: role, message, agent, timestamp
        if not history:
             self.append_system_message("Witaj w HexStrike Nexus. Wybierz agenta i rozpocznij operację.")
             return

        for row in history:
            role, message, agent, timestamp = row
            if role == "User":
                self.display_message("Ty", message, "#007bff")
            elif role == "Nexus":
                self.display_message("Nexus", message, "#28a745")
            else:
                self.display_message("System", message, "#6c757d")

    def set_server_status(self, is_online):
        if is_online:
            self.status_label.setText("HexStrike: ONLINE")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.status_label.setText("HexStrike: OFFLINE")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")

    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return

        agent = self.agent_selector.currentText()
        lang = self.lang_selector.currentText()

        # Display and Save User Message
        self.append_user_message(user_text, agent)
        self.input_field.clear()

        # Process with AI
        response = self.ai_client.process_user_request(user_text, agent, language="pl" if lang == "Polski" else "en")

        # Display and Save AI Message
        self.append_ai_message(response, agent)

    def append_user_message(self, text, agent):
        self.display_message("Ty", text, "#007bff")
        self.db.add_message("User", text, agent)

    def append_ai_message(self, html, agent):
        self.display_message("Nexus", html, "#28a745")
        self.db.add_message("Nexus", html, agent)

    def append_system_message(self, text):
        self.display_message("System", text, "#6c757d")
        # System messages might not be saved or optional

    def display_message(self, role, text, color):
        div = f"<div style='color: {color}; margin-bottom: 10px;'><b>{role}:</b><br>{text}</div>"

        if HAS_WEBENGINE and hasattr(self.chat_display, 'setHtml'):
            self.html_content += div
            self.chat_display.setHtml(self.html_content + "</body></html>")
            # Scroll to bottom using JS
            self.chat_display.page().runJavaScript("window.scrollTo(0, document.body.scrollHeight);")
        else:
            # QTextBrowser logic
            # append automatically adds new line
            self.chat_display.append(div)
