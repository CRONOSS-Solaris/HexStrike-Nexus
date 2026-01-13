import subprocess
import sys
import time
import requests
from .config import Config

class HexStrikeManager:
    def __init__(self):
        self.process = None

    def start_server(self):
        """Starts the HexStrike Server in the background."""
        if self.is_running():
            print("HexStrike Server is already running.")
            return

        print(f"Starting HexStrike Server from {Config.SERVER_SCRIPT_PATH}...")
        try:
            self.process = subprocess.Popen(
                [sys.executable, Config.SERVER_SCRIPT_PATH],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Wait a bit for server to start
            for _ in range(10):
                if self.is_running():
                    print("HexStrike Server started successfully.")
                    return
                time.sleep(0.5)

            print("Warning: HexStrike Server might not have started correctly.")
            # Check if process is dead
            if self.process.poll() is not None:
                print(f"Server process died with return code {self.process.returncode}")
        except Exception as e:
            print(f"Failed to start server: {e}")

    def stop_server(self):
        """Stops the HexStrike Server."""
        if self.process:
            self.process.terminate()
            self.process = None
            print("HexStrike Server stopped.")

    def is_running(self):
        """Checks if the server is responsive via the health endpoint."""
        try:
            response = requests.get(f"{Config.SERVER_URL}/health", timeout=1)
            return response.status_code == 200
        except requests.RequestException:
            return False
