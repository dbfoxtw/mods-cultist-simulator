import json
from file_set import FileSet
from json_file import JsonFile

class MainModel:
    def __init__(self):
        self.english_file_set = FileSet()
        self.chinese_file_set = FileSet()
        self.english_json = JsonFile()
        self.chinese_json = JsonFile()

# region Folder
    def set_english_folder(self, path):
        self.english_file_set.set_folder(path)
        self._update_english_file()

    def set_chinese_folder(self, path):
        self.chinese_file_set.set_folder(path)
        self._update_chinese_file()
# endregion

# region File
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
        self._update_both_files()

    def next_file(self):
        self.english_file_set.next_file()
        new_filename = self.english_file_set.get_current_filename()
        self.chinese_file_set.jump_to_file_by_name(new_filename)
        self._update_both_files()

    def jump_to_file_by_name(self, filename):
        file_exist = self.english_file_set.jump_to_file_by_name(filename)
        if file_exist:
            self.chinese_file_set.jump_to_file_by_name(filename)
            self._update_both_files()
            return True
        else:
            return False
        
    def _update_english_file(self):
        self.english_json.clear()
        file_path = self.english_file_set.get_current_file_path()
        if file_path:
            self.english_json.parse(file_path)

    def _update_chinese_file(self):
        self.chinese_json.clear()
        file_path = self.chinese_file_set.get_current_file_path()
        if file_path:
            self.chinese_json.parse(file_path)
            self._update_chinese_entry()
    
    def _update_both_files(self):
        self._update_english_file()
        self._update_chinese_file()
# endregion

# region Entry
    def _update_chinese_entry(self):
        current_id = self.get_current_entry_id()
        if current_id:
            self.chinese_json.find_entry(current_id)

    def get_current_entry_id(self):
        return self.english_json.get_current_entry_id()

    def prev_entry(self):
        self.english_json.prev_entry()
        self._update_chinese_entry()

    def next_entry(self):
        self.english_json.next_entry()
        self._update_chinese_entry()

    def get_english_entry_content(self):
        return self.english_json.get_entry_content()
    
    def get_chinese_entry_content(self):
        return self.chinese_json.get_entry_content()
    
    def get_current_index(self):
        return self.english_json.get_current_index()

    def get_entry_count(self):
        return self.english_json.get_entry_count()
        
# endregion