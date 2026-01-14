import os
import json

class Config:
    VERSION = "1.0.0"

    # Load language from config
    LANGUAGE = "en"
    HEXSTRIKE_CONFIG = os.path.expanduser("~/.hexstrike/config.json")
    if os.path.exists(HEXSTRIKE_CONFIG):
        try:
            with open(HEXSTRIKE_CONFIG, "r") as f:
                data = json.load(f)
                LANGUAGE = data.get("language", "en")
        except:
            pass

    SERVER_PORT = 8888
    SERVER_URL = f"http://localhost:{SERVER_PORT}"

    HEXSTRIKE_CORE_DIR = os.path.expanduser("~/.hexstrike/core")
    REAL_SERVER_PATH = os.path.join(HEXSTRIKE_CORE_DIR, "hexstrike_server.py")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MOCK_SERVER_PATH = os.path.join(BASE_DIR, "mock_server.py")
    
    # Icons directory - absolute path (icons are in hexstrike_nexus/icons, not dashboard/icons)
    # __file__ is in dashboard/core/config.py, so we go up 3 levels to hexstrike_nexus root
    ICONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "icons")

    # Use real server if available, otherwise use mock
    SERVER_SCRIPT_PATH = REAL_SERVER_PATH if os.path.exists(REAL_SERVER_PATH) else MOCK_SERVER_PATH
    
    @staticmethod
    def save_language(language: str):
        """Save language preference to config file"""
        Config.LANGUAGE = language
        
        # Ensure directory exists
        config_dir = os.path.dirname(Config.HEXSTRIKE_CONFIG)
        os.makedirs(config_dir, exist_ok=True)
        
        # Load existing config or create new
        config_data = {}
        if os.path.exists(Config.HEXSTRIKE_CONFIG):
            try:
                with open(Config.HEXSTRIKE_CONFIG, "r") as f:
                    config_data = json.load(f)
            except:
                pass
        
        # Update language
        config_data["language"] = language
        
        # Save config
        with open(Config.HEXSTRIKE_CONFIG, "w") as f:
            json.dump(config_data, f, indent=2)

