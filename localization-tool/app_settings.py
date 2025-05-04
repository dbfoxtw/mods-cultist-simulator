import os
import json

class AppSettings:
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        self.original_folder_path = ""
        self.translated_folder_path = ""

    def save_settings(self):
        data = {
            "original_folder": self.original_folder_path,
            "translated_folder": self.translated_folder_path
        }
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.original_folder_path = data.get("original_folder", "")
                self.translated_folder_path = data.get("translated_folder", "")