import os

class Config:
    VERSION = "1.0.0"
    SERVER_PORT = 8888
    SERVER_URL = f"http://localhost:{SERVER_PORT}"

    HEXSTRIKE_CORE_DIR = os.path.expanduser("~/.hexstrike/core")
    REAL_SERVER_PATH = os.path.join(HEXSTRIKE_CORE_DIR, "hexstrike_server.py")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MOCK_SERVER_PATH = os.path.join(BASE_DIR, "mock_server.py")

    # Use real server if available, otherwise use mock
    SERVER_SCRIPT_PATH = REAL_SERVER_PATH if os.path.exists(REAL_SERVER_PATH) else MOCK_SERVER_PATH
