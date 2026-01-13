import json
import os
import sys

class LanguageManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance.translations = {}
            cls._instance.current_lang = "en"

            # Determine base path relative to this file
            cls._instance.base_path = os.path.dirname(os.path.abspath(__file__))
            cls._instance.locales_path = os.path.join(cls._instance.base_path, "locales")

        return cls._instance

    def load_language(self, lang_code):
        if lang_code not in ["en", "pl"]:
            lang_code = "en" # Fallback

        json_path = os.path.join(self.locales_path, f"{lang_code}.json")
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
            self.current_lang = lang_code
            return True
        except FileNotFoundError:
            print(f"[-] Language file not found: {json_path}")
            return False
        except json.JSONDecodeError:
            print(f"[-] Invalid JSON in language file: {json_path}")
            return False

    def get(self, key, **kwargs):
        val = self.translations.get(key, key)
        if kwargs:
            try:
                return val.format(**kwargs)
            except (KeyError, ValueError, IndexError):
                return val
        return val

# Global instance
i18n = LanguageManager()
