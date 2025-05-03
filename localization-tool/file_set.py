import os

class FileSet:
    def __init__(self, folder_path=""):
        self.folder_path = folder_path
        self._files = []
        self._current_file_index = 0

    def set_folder(self, path):
        self.folder_path = path
        self._load_files()

    def _load_files(self):
        if os.path.isdir(self.folder_path):
            self._files = [f for f in os.listdir(self.folder_path) if f.endswith('.json')]
            self._files.sort()
            self._file_index = 0

    def get_total_files(self):
        return len(self._files)

    def get_current_filename(self):
        if self._files:
            return self._files[self._file_index]
        return ""

    def is_first_file(self):
        return self._file_index == 0
    
    def is_last_file(self):
        return self._file_index >= len(self._files) - 1

    def prev_file(self):
        if not self.is_first_file():
            self._file_index -= 1

    def next_file(self):
        if not self.is_last_file():
            self._file_index += 1

    def jump_to_file_by_name(self, filename):
        if filename in self._files:
            self._file_index = self._files.index(filename)
            return True
        return False
