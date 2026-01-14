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
        
        self.host_input = QLineEdit("localhost") # Config.HOST not available, defaulting to localhost
        self.port_input = QLineEdit(str(Config.SERVER_PORT))
        
        form.addRow(QLabel("Server Host:"), self.host_input)
        form.addRow(QLabel("Server Port:"), self.port_input)
        
        group.setLayout(form)
        self.layout.addWidget(group)

    def create_appearance_group(self):
        group = QGroupBox(i18n.get("settings_group_appearance", default="Appearance"))
        vbox = QVBoxLayout()
        vbox.setContentsMargins(20, 25, 20, 20)
        
        # Language selection with dropdown
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Language:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("Polski", "pl")
        
        # Set current language
        current_lang = Config.LANGUAGE
        index = 0 if current_lang == "en" else 1
        self.lang_combo.setCurrentIndex(index)
        
        lang_layout.addWidget(self.lang_combo)
        
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
        # Get selected language code from combobox
        selected_lang = self.lang_combo.currentData()
        
        # Save language using Config
        if selected_lang and selected_lang != Config.LANGUAGE:
            Config.save_language(selected_lang)
            
            # Reload i18n with new language
            i18n.load_language(selected_lang)
            
            # Notify user that language was changed
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "Settings Saved" if selected_lang == "en" else "Zapisano Ustawienia",
                "Language changed successfully. Some UI elements will update immediately." if selected_lang == "en" 
                else "Język został zmieniony pomyślnie. Niektóre elementy interfejsu zaktualizują się natychmiast."
            )
            
            # Update UI labels with new language
            self.findChild(QLabel).setText(i18n.get("settings_title", default="Settings"))
        
        # Save other settings
        print("Settings Saved:")
        print(f"Host: {self.host_input.text()}")
        print(f"Port: {self.port_input.text()}")
        print(f"Language: {selected_lang}")

