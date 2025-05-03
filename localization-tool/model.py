import json
import os

class MainModel:
    def __init__(self):
        self.english_folder = ""
        self.chinese_folder = ""
        self.files = []
        self.current_file_index = 0
        self.current_id = ""

    def set_english_folder(self, path):
        self.english_folder = path
        self._load_file_list()

    def set_chinese_folder(self, path):
        self.chinese_folder = path

    def _load_file_list(self):
        if os.path.isdir(self.english_folder):
            self.files = [f for f in os.listdir(self.english_folder) if f.endswith('.json')]
            self.files.sort()
            self.current_file_index = 0

    def get_total_files(self):
        return len(self.files)

    def get_current_filename(self):
        if self.files:
            return self.files[self.current_file_index]
        return ""

    def load_current_json(self):
        if not self.files:
            return {}
        path = os.path.join(self.english_folder, self.files[self.current_file_index])
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"讀取 JSON 錯誤: {e}")
            return {}

    def next_file(self):
        if self.current_file_index < len(self.files) - 1:
            self.current_file_index += 1

    def prev_file(self):
        if self.current_file_index > 0:
            self.current_file_index -= 1

    def jump_to_file(self, index):
        if 0 <= index < len(self.files):
            self.current_file_index = index
