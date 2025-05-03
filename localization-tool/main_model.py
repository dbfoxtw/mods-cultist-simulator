import json
from file_set import FileSet

class MainModel:
    def __init__(self):
        self.english_file_set = FileSet()
        self.chinese_file_set = FileSet()
        self.current_id = ""

    def set_english_folder(self, path):
        self.english_file_set.set_folder(path)

    def set_chinese_folder(self, path):
        self.chinese_file_set.set_folder(path)

    def get_current_filename(self):
        return self.english_file_set.get_current_filename()
    
    def is_first_file(self):
        return self.english_file_set.is_first_file()
    
    def is_last_file(self):
        return self.english_file_set.is_last_file()

    def prev_file(self):
        self.english_file_set.prev_file()
        new_filename = self.english_file_set.get_current_filename()
        self.chinese_file_set.jump_to_file_by_name(new_filename)

    def next_file(self):
        self.english_file_set.next_file()
        new_filename = self.english_file_set.get_current_filename()
        self.chinese_file_set.jump_to_file_by_name(new_filename)

    def jump_to_file_by_name(self, filename):
        file_exist = self.english_file_set.jump_to_file_by_name(filename)
        if file_exist:
            self.chinese_file_set.jump_to_file_by_name(filename)
            return True
        else:
            return False