try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QProgressBar,
                                 QListWidget, QGroupBox, QFormLayout)
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
    class QGroupBox:
        def setLayout(self, l): pass
    class QFormLayout:
        def addRow(self, l, w): pass

class TelemetryWidget(QWidget):
    def __init__(self):
        super().__init__()
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

        layout.addWidget(stats_group)

        # Active Processes
        proc_group = QGroupBox("Aktywne Procesy")
        proc_layout = QVBoxLayout()
        proc_group.setLayout(proc_layout)

        self.process_list = QListWidget()
        proc_layout.addWidget(self.process_list)

        layout.addWidget(proc_group)

        # Live Console
        log_group = QGroupBox("Live Console")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)

        self.log_display = QListWidget()
        self.log_display.setStyleSheet("background-color: black; color: #00FF00; font-family: monospace;")
        log_layout.addWidget(self.log_display)

        layout.addWidget(log_group)

    def update_data(self, data):
        """
        data = {
            "cpu_usage": int,
            "ram_usage": int,
            "cache_hits": int,
            "active_processes": [{"pid": int, "name": str, "status": str}, ...]
        }
        """
        self.cpu_bar.setValue(data.get("cpu_usage", 0))
        self.ram_bar.setValue(data.get("ram_usage", 0))
        self.cache_hits_label.setText(str(data.get("cache_hits", 0)))

        self.process_list.clear()
        for proc in data.get("active_processes", []):
            self.process_list.addItem(f"[{proc.get('pid')}] {proc.get('name')} - {proc.get('status')}")

    def update_logs(self, log_data):
        """
        log_data = {"logs": ["line1", "line2"]}
        """
        if not log_data:
            return

        logs = log_data.get("logs", [])
        for line in logs:
            self.log_display.addItem(line)

        # Keep log buffer reasonable size
        if self.log_display.count() > 1000:
            # Not easy to remove from top in QListWidget efficiently without loop, but for now ok
            pass

        self.log_display.scrollToBottom()
