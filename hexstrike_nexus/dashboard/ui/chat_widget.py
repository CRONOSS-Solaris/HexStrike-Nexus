try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser,
                                 QLineEdit, QPushButton, QComboBox, QLabel)
    from PyQt6.QtCore import Qt
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
    class QLineEdit:
        def text(self): return ""
        def clear(self): pass
        def returnPressed(self): pass
        def connect(self, f): pass # Mocking signal
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

from ..core.ai_client import AIClient

class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ai_client = AIClient()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Header: Status & Agent Selector
        header_layout = QHBoxLayout()

        self.status_label = QLabel("HexStrike: DISCONNECTED")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        header_layout.addWidget(self.status_label)

        header_layout.addStretch()

        layout.addWidget(QLabel("Wybierz Agenta:"))
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

        # Welcome message
        self.append_system_message("Witaj w HexStrike Nexus. Wybierz agenta i rozpocznij operację.")

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

        self.append_user_message(user_text)
        self.input_field.clear()

        # Process with AI
        agent = self.agent_selector.currentText()
        response = self.ai_client.process_user_request(user_text, agent)
        self.append_ai_message(response)

    def append_user_message(self, text):
        self.chat_display.append(f"<div style='color: #007bff;'><b>Ty:</b> {text}</div>")

    def append_ai_message(self, html):
        self.chat_display.append(f"<div style='color: #28a745;'><b>Nexus:</b><br>{html}</div>")

    def append_system_message(self, text):
        self.chat_display.append(f"<div style='color: #6c757d;'><i>{text}</i></div>")
