try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QProgressBar,
                                 QListWidget, QGroupBox, QFormLayout, QMenu)
    from PyQt6.QtCore import Qt
except ImportError:
    class QWidget:
        def setLayout(self, l): pass
    class QVBoxLayout:
        def addWidget(self, w): pass
    class QLabel:
        def setText(self, t): pass
    class QProgressBar:
        def setValue(self, v): pass
    class QListWidget:
        def clear(self): pass
        def addItem(self, i): pass
        def count(self): return 0
        def scrollToBottom(self): pass
        def setContextMenuPolicy(self, p): pass
        def itemAt(self, p): return None
        def mapToGlobal(self, p): return p
    class QGroupBox:
        def setLayout(self, l): pass
    class QFormLayout:
        def addRow(self, l, w): pass
    class QMenu:
        def addAction(self, t): return "action"
        def exec(self, p): return "action"
    class Qt:
        class ContextMenuPolicy:
            CustomContextMenu = 1

from ..core.api_client import APIClient

class TelemetryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("TelemetryWidget")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Resources
        res_group = QGroupBox("Zasoby Systemowe")
        res_layout = QFormLayout()
        res_group.setLayout(res_layout)

        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        res_layout.addRow("CPU:", self.cpu_bar)

        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        res_layout.addRow("RAM:", self.ram_bar)

        layout.addWidget(res_group)

        # Stats
        stats_group = QGroupBox("Statystyki HexStrike")
        stats_layout = QFormLayout()
        stats_group.setLayout(stats_layout)

        self.cache_hits_label = QLabel("0")
        stats_layout.addRow("Cache Hits:", self.cache_hits_label)

        self.cache_misses_label = QLabel("0")
        stats_layout.addRow("Cache Misses:", self.cache_misses_label)

        self.cache_size_label = QLabel("0 MB")
        stats_layout.addRow("Cache Size:", self.cache_size_label)

        layout.addWidget(stats_group)

        # Active Processes
        proc_group = QGroupBox("Aktywne Procesy")
        proc_layout = QVBoxLayout()
        proc_group.setLayout(proc_layout)

        self.process_list = QListWidget()
        # Enable context menu
        try:
            self.process_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.process_list.customContextMenuRequested.connect(self.show_process_context_menu)
        except AttributeError:
            pass # Sandbox fallback

        proc_layout.addWidget(self.process_list)

        layout.addWidget(proc_group)

        # Live Console
        log_group = QGroupBox("Live Console")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)

        self.log_display = QListWidget()
        self.log_display.setStyleSheet("background-color: #0f111a; color: #00e676; font-family: monospace; border: 1px solid #2f344a;")
        log_layout.addWidget(self.log_display)

        layout.addWidget(log_group)

    def show_process_context_menu(self, pos):
        item = self.process_list.itemAt(pos)
        if not item: return

        menu = QMenu()
        kill_action = menu.addAction("Terminate Process")
        action = menu.exec(self.process_list.mapToGlobal(pos))

        if action == kill_action:
            self.terminate_selected_process(item)

    def terminate_selected_process(self, item):
        # Parse PID from string "[4021] masscan..."
        text = item.text()
        try:
            pid_str = text.split(']')[0].strip('[')
            APIClient.terminate_process(pid_str)
            # Remove item from list immediately for feedback, though next update will sync
            # self.process_list.takeItem(self.process_list.row(item))
        except:
            pass

    def update_data(self, data):
        self.cpu_bar.setValue(data.get("cpu_usage", 0))
        self.ram_bar.setValue(data.get("ram_usage", 0))
        # Telemetry endpoint also has cache_hits, we use it here or override with cache stats
        self.cache_hits_label.setText(str(data.get("cache_hits", 0)))

        # Only update process list if we are not hovering/interacting to avoid flicker?
        # For simplicity, we just clear and add.
        # Ideally, we diff the list.
        self.process_list.clear()
        for proc in data.get("active_processes", []):
            self.process_list.addItem(f"[{proc.get('pid')}] {proc.get('name')} - {proc.get('status')}")

    def update_cache_stats(self, stats):
        """
        stats = {"hits": int, "misses": int, "size_mb": float}
        """
        if not stats: return
        self.cache_hits_label.setText(str(stats.get("hits", 0)))
        self.cache_misses_label.setText(str(stats.get("misses", 0)))
        self.cache_size_label.setText(f"{stats.get('size_mb', 0):.2f} MB")

    def update_logs(self, log_data):
        if not log_data:
            return

        logs = log_data.get("logs", [])
        for line in logs:
            self.log_display.addItem(line)

        if self.log_display.count() > 1000:
            pass

        self.log_display.scrollToBottom()
