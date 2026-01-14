from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QListWidget, QStackedWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon

from .chat_widget import ChatWidget
from .telemetry_widget import TelemetryWidget
from .settings_widget import SettingsWidget
from .styles import HexStyle
from ..core.api_client import APIClient
from ..core.config import Config
from ...i18n.manager import i18n

class MainWindow(QMainWindow):
    def __init__(self, server_manager):
        super().__init__()
        # Load language from config
        i18n.load_language(Config.LANGUAGE)

        self.server_manager = server_manager
        self.setWindowTitle(i18n.get("window_title", version=Config.VERSION))
        self.resize(1280, 850)

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
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # --- Sidebar (Left) ---
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(250)
        self.sidebar.currentRowChanged.connect(self.display_page)
        
        # Add Items to Sidebar
        items = [
            ("Chat Agent", "chat_icon.png"),     # 0
            ("Telemetry", "chart_icon.png"),     # 1
            ("Settings", "settings_icon.png")    # 2
        ]
        
        for name, icon in items:
            item = QListWidgetItem(name)
            # item.setIcon(QIcon(icon)) # TODO: Add real icons
            item.setSizeHint(QSize(200, 50))
            self.sidebar.addItem(item)
            
        main_layout.addWidget(self.sidebar)

        # --- Content Area (Right) ---
        self.content_area = QWidget()
        self.content_area.setObjectName("ContentArea")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_area.setLayout(content_layout)
        
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        
        main_layout.addWidget(self.content_area)

        # Initialize Widgets
        self.chat_widget = ChatWidget()
        self.telemetry_widget = TelemetryWidget()
        self.settings_widget = SettingsWidget()
        
        # Add to Stack
        self.stack.addWidget(self.chat_widget)      # Index 0
        self.stack.addWidget(self.telemetry_widget) # Index 1
        self.stack.addWidget(self.settings_widget)  # Index 2
        
        # Default Selection
        self.sidebar.setCurrentRow(0)

    def display_page(self, index):
        self.stack.setCurrentIndex(index)

    def update_status(self):
        # Update server status indicator
        if self.server_manager.is_running():
            self.chat_widget.set_server_status(True)
            
            # Only update telemetry if it's visible to save resources
            if self.stack.currentIndex() == 1:
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
