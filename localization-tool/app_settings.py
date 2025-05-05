import os
import json

class AppSettings:
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        self.original_folder_path = ""
        self.translated_folder_path = ""
        self.proper_nouns = []

    def save_settings(self):
        data = {
            "original_folder": self.original_folder_path,
            "translated_folder": self.translated_folder_path,
            "proper_nouns": self.proper_nouns
        }
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.original_folder_path = data.get("original_folder", "")
                self.translated_folder_path = data.get("translated_folder", "")
                self.proper_nouns = data.get("proper_nouns", [])

    def add_proper_noun(self, word):
        word = word.strip()
        if word and word not in self.proper_nouns:
            self.proper_nouns.append(word)
            self.save_settings()

    def remove_proper_noun(self, word):
        if word in self.proper_nouns:
            self.proper_nouns.remove(word)
            self.save_settings()

    def get_proper_nouns(self):
        return self.proper_nouns

    def extract_proper_nouns_from_text(self, text):
        return [word for word in self.proper_nouns if word in text]
