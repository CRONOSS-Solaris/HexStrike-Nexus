import sys
import os
import signal

# Ensure the package can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hexstrike_nexus.dashboard.app import HexStrikeDashboardApp

def main():
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = HexStrikeDashboardApp(sys.argv)
    sys.exit(app.run())

if __name__ == "__main__":
    main()
