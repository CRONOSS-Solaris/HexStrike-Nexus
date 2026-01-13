try:
    from PyQt6.QtWidgets import QApplication
except ImportError:
    # Fallback for environments without PyQt6 (like this sandbox maybe)
    # This allows me to at least syntax check the rest of the file if I were running it
    class QApplication:
        def __init__(self, argv): pass
        def exec(self): return 0
        def quit(self): pass

from .ui.main_window import MainWindow
from .core.hexstrike_manager import HexStrikeManager
from .core.update_manager import UpdateManager
import threading
import time

class HexStrikeDashboardApp:
    def __init__(self, argv):
        self.app = QApplication(argv)
        self.manager = HexStrikeManager()
        self.main_window = None

    def run(self):
        print("Initializing HexStrike Nexus...")

        # Check for updates
        if UpdateManager.check_for_updates():
            print("Updates applied. Please restart the application.")
            return 0

        # Start the HexStrike Server
        self.manager.start_server()

        # Initialize UI
        self.main_window = MainWindow(self.manager)
        self.main_window.show()

        # Run event loop
        exit_code = self.app.exec()

        # Cleanup
        print("Shutting down HexStrike Nexus...")
        self.manager.stop_server()

        return exit_code
