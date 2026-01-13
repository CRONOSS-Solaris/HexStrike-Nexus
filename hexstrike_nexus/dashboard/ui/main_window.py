try:
    from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                                 QLabel, QComboBox, QPushButton, QSplitter)
    from PyQt6.QtCore import Qt, QTimer
except ImportError:
    # Dummy classes for validation in sandbox
    class QMainWindow:
        def setCentralWidget(self, w): pass
        def show(self): pass
        def setWindowTitle(self, t): pass
        def resize(self, w, h): pass
        def closeEvent(self, e): pass
    class QWidget:
        def setLayout(self, l): pass
    class QHBoxLayout:
        def addWidget(self, w): pass
        def setContentsMargins(self, a,b,c,d): pass
    class QVBoxLayout:
        def addWidget(self, w): pass
        def addLayout(self, l): pass
        def setContentsMargins(self, a,b,c,d): pass
    class QLabel:
        def setText(self, t): pass
        def setStyleSheet(self, s): pass
    class QComboBox:
        def addItems(self, i): pass
        def currentText(self): return ""
    class QPushButton:
        def clicked(self): pass
    class QSplitter:
        def addWidget(self, w): pass
        def setStretchFactor(self, i, f): pass
    class Qt:
        Horizontal = 1
    class QTimer:
        timeout = None
        def start(self, ms): pass
        def connect(self, f): pass

from .chat_widget import ChatWidget
from .telemetry_widget import TelemetryWidget
from .styles import HexStyle
from ..core.api_client import APIClient
from ..core.config import Config

class MainWindow(QMainWindow):
    def __init__(self, server_manager):
        super().__init__()
        self.server_manager = server_manager
        self.setWindowTitle(f"HexStrike Nexus v{Config.VERSION}")
        self.resize(1200, 800)

        # Apply Global Styles
        self.setStyleSheet(HexStyle.APP_STYLE)

        self.init_ui()

        # Timer for health check / telemetry update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000) # Every 2 seconds

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Chat Panel (Left/Center)
        self.chat_widget = ChatWidget()
        splitter.addWidget(self.chat_widget)

        # Telemetry Panel (Right)
        self.telemetry_widget = TelemetryWidget()
        splitter.addWidget(self.telemetry_widget)

        splitter.setStretchFactor(0, 3) # Chat takes more space
        splitter.setStretchFactor(1, 1)

    def update_status(self):
        # Update server status indicator
        if self.server_manager.is_running():
            self.chat_widget.set_server_status(True)
            # Fetch telemetry
            data = APIClient.get_telemetry()
            if data:
                self.telemetry_widget.update_data(data)

            # Fetch logs
            logs = APIClient.get_logs()
            if logs:
                self.telemetry_widget.update_logs(logs)

            # Fetch Cache Stats
            cache_stats = APIClient.get_cache_stats()
            if cache_stats:
                self.telemetry_widget.update_cache_stats(cache_stats)
        else:
            self.chat_widget.set_server_status(False)

    def closeEvent(self, event):
        # Ensure server is stopped when window closes
        self.server_manager.stop_server()
        event.accept()
