try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
                                 QListWidget, QGroupBox, QFormLayout, QMenu, QGridLayout, QFrame)
    from PyQt6.QtCore import Qt
except ImportError:
    # ... (Mocks for non-PyQt environments)
    class QWidget: pass
    class QVBoxLayout:
        def addWidget(self, w): pass
        def addLayout(self, l): pass
    class QHBoxLayout:
        def addWidget(self, w): pass
    class QGridLayout:
        def addWidget(self, w, r, c): pass
    class QLabel:
        def setText(self, t): pass
        def setStyleSheet(self, s): pass
    class QProgressBar:
        def setValue(self, v): pass
    class QListWidget:
        def clear(self): pass
        def addItem(self, i): pass
        def count(self): return 0
        def scrollToBottom(self): pass
        def setContextMenuPolicy(self, p): pass
    class QGroupBox:
        def setLayout(self, l): pass
    class QMenu: pass
    class QFrame: pass
    class Qt:
        class ContextMenuPolicy:
            CustomContextMenu = 1

from ..core.api_client import APIClient
from ...i18n.manager import i18n
from .styles import HexStyle

class TelemetryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("TelemetryWidget")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(20)

        # Title
        title = QLabel(i18n.get("telemetry_title", default="Dashboard Telemetry"))
        title.setObjectName("HeaderTitle")
        layout.addWidget(title)

        # --- Top Grid: Stats Cards ---
        grid = QGridLayout()
        grid.setSpacing(15)

        # CPU Card
        self.cpu_card = self.create_stat_card("CPU Usage", "0%", HexStyle.STATUS_WARNING)
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setTextVisible(False)
        self.cpu_bar.setFixedHeight(6)
        # Hacky way to insert bar into card, effectively just recreating it for simplicity or adding to layout
        # For simplicity, we'll just keep the card simple and update label text
        grid.addWidget(self.cpu_card, 0, 0)

        # RAM Card
        self.ram_card = self.create_stat_card("RAM Usage", "0%", HexStyle.ACCENT_SECONDARY)
        grid.addWidget(self.ram_card, 0, 1)

        # Cache Hits
        self.cache_hits_card = self.create_stat_card("Cache Hits", "0", HexStyle.STATUS_SUCCESS)
        grid.addWidget(self.cache_hits_card, 1, 0)
        
        # Cache Misses
        self.cache_misses_card = self.create_stat_card("Cache Misses", "0", HexStyle.STATUS_ERROR)
        grid.addWidget(self.cache_misses_card, 1, 1)
        
        # Cache Size
        self.cache_size_card = self.create_stat_card("Cache Size", "0 MB", HexStyle.TEXT_PRIMARY)
        grid.addWidget(self.cache_size_card, 1, 2)

        layout.addLayout(grid)

        # --- Active Processes ---
        proc_group = QGroupBox(i18n.get("active_processes"))
        proc_layout = QVBoxLayout()
        proc_group.setLayout(proc_layout)

        self.process_list = QListWidget()
        self.process_list.setStyleSheet(f"background-color: {HexStyle.BG_INPUT}; border-radius: 6px;")
        
        try:
            self.process_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.process_list.customContextMenuRequested.connect(self.show_process_context_menu)
        except AttributeError:
            pass 

        proc_layout.addWidget(self.process_list)
        layout.addWidget(proc_group)

        # --- Live Console (Logs) ---
        log_group = QGroupBox(i18n.get("live_console"))
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)

        self.log_display = QListWidget()
        self.log_display.setStyleSheet(f"background-color: {HexStyle.BG_MAIN}; color: {HexStyle.STATUS_SUCCESS}; font-family: 'Consolas', monospace; border: 1px solid {HexStyle.BORDER_LIGHT}; border-radius: 6px;")
        log_layout.addWidget(self.log_display)

        layout.addWidget(log_group)

    def create_stat_card(self, title_text, value_text, color_code):
        frame = QFrame()
        frame.setObjectName("Card") # Uses generic card style
        frame.setStyleSheet(f"background-color: {HexStyle.BG_CARD}; border-radius: 12px; border: 1px solid {HexStyle.BORDER_LIGHT};")
        
        layout = QVBoxLayout(frame)
        
        title = QLabel(title_text)
        title.setStyleSheet(f"color: {HexStyle.TEXT_SECONDARY}; font-size: 12px; font-weight: bold;")
        layout.addWidget(title)
        
        value = QLabel(value_text)
        value.setStyleSheet(f"color: {color_code}; font-size: 24px; font-weight: bold;")
        layout.addWidget(value)
        
        # Store reference to value label on the frame object for easy updating
        frame.value_label = value
        return frame

    def show_process_context_menu(self, pos):
        item = self.process_list.itemAt(pos)
        if not item: return

        menu = QMenu()
        kill_action = menu.addAction("Terminate Process")
        action = menu.exec(self.process_list.mapToGlobal(pos))

        if action == kill_action:
            self.terminate_selected_process(item)

    def terminate_selected_process(self, item):
        text = item.text()
        try:
            pid_str = text.split(']')[0].strip('[')
            APIClient.terminate_process(pid_str)
        except:
            pass

    def update_data(self, data):
        # Update Cards
        cpu_val = data.get("cpu_usage", 0)
        self.cpu_card.value_label.setText(f"{cpu_val}%")
        
        ram_val = data.get("ram_usage", 0)
        self.ram_card.value_label.setText(f"{ram_val}%")

        self.cache_hits_card.value_label.setText(str(data.get("cache_hits", 0)))
        
        # Process List
        self.process_list.clear()
        for proc in data.get("active_processes", []):
            self.process_list.addItem(f"[{proc.get('pid')}] {proc.get('name')} - {proc.get('status')}")

    def update_cache_stats(self, stats):
        if not stats: return
        self.cache_hits_card.value_label.setText(str(stats.get("hits", 0)))
        self.cache_misses_card.value_label.setText(str(stats.get("misses", 0)))
        self.cache_size_card.value_label.setText(f"{stats.get('size_mb', 0):.2f} MB")

    def update_logs(self, log_data):
        if not log_data:
            return

        logs = log_data.get("logs", [])
        for line in logs:
            self.log_display.addItem(line)

        self.log_display.scrollToBottom()
