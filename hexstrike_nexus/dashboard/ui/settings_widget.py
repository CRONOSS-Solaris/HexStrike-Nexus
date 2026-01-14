from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QCheckBox, QGroupBox, QPushButton, QFormLayout)
from PyQt6.QtCore import Qt
from .styles import HexStyle
from ...i18n.manager import i18n
from ..core.config import Config

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        # Header
        title = QLabel(i18n.get("settings_title", default="Settings"))
        title.setObjectName("HeaderTitle")
        self.layout.addWidget(title)
        
        # Connection Settings
        self.create_connection_group()
        
        # Appearance Settings
        self.create_appearance_group()
        
        self.layout.addStretch()
        
        # Save Button
        save_btn = QPushButton(i18n.get("settings_save", default="Save Configuration"))
        save_btn.setMinimumHeight(40)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.save_settings)
        self.layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)

    def create_connection_group(self):
        group = QGroupBox(i18n.get("settings_group_connection", default="Connection"))
        form = QFormLayout()
        form.setContentsMargins(20, 25, 20, 20)
        form.setSpacing(15)
        
        self.host_input = QLineEdit(Config.HOST)
        self.port_input = QLineEdit(str(Config.PORT))
        
        form.addRow(QLabel("Server Host:"), self.host_input)
        form.addRow(QLabel("Server Port:"), self.port_input)
        
        group.setLayout(form)
        self.layout.addWidget(group)

    def create_appearance_group(self):
        group = QGroupBox(i18n.get("settings_group_appearance", default="Appearance"))
        vbox = QVBoxLayout()
        vbox.setContentsMargins(20, 25, 20, 20)
        
        # Language (Mockup for now as it requires restart)
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Language:"))
        self.lang_input = QLineEdit(Config.LANGUAGE)
        self.lang_input.setPlaceholderText("pl / en")
        lang_layout.addWidget(self.lang_input)
        
        vbox.addLayout(lang_layout)
        
        # Theme Toggle (Placeholder)
        self.dark_mode_cb = QCheckBox("Dark Mode Enabled")
        self.dark_mode_cb.setChecked(True)
        self.dark_mode_cb.setEnabled(False) # Forced for now
        vbox.addWidget(self.dark_mode_cb)
        
        group.setLayout(vbox)
        self.layout.addWidget(group)

    def save_settings(self):
        # Logic to save to Config or file
        # For now just print
        print("Settings Saved:")
        print(f"Host: {self.host_input.text()}")
        print(f"Port: {self.port_input.text()}")
        # In a real app, we would write to .env or config.py
