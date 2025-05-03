import os
import json

class AppSettings:
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        self.english_folder_path = ""
        self.chinese_folder_path = ""

    def save_settings(self):
        data = {
            "english_folder": self.english_folder_path,
            "chinese_folder": self.chinese_folder_path
        }
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.english_folder_path = data.get("english_folder", "")
                self.chinese_folder_path = data.get("chinese_folder", "")