import json
from file_set import FileSet
from json_file import JsonFile

class MainModel:
    def __init__(self):
        self.original_file_set = FileSet()
        self.translated_file_set = FileSet()
        self.original_json = JsonFile()
        self.translated_json = JsonFile()

# region Folder
    def set_original_folder(self, path):
        self.original_file_set.set_folder(path)
        self._update_original_file()

    def set_translated_folder(self, path):
        self.translated_file_set.set_folder(path)
        self._update_translated_file()
# endregion

# region File
    def get_current_filename(self):
        return self.original_file_set.get_current_filename()
    
    def is_first_file(self):
        return self.original_file_set.is_first_file()
    
    def is_last_file(self):
        return self.original_file_set.is_last_file()

    def reload_file(self):
        current_id = self.get_current_entry_id()
        self._update_both_files()
        self.jump_to_index_by_id(current_id)

    def prev_file(self):
        self.original_file_set.prev_file()
        new_filename = self.original_file_set.get_current_filename()
        self.translated_file_set.jump_to_file_by_name(new_filename)
        self._update_both_files()

    def next_file(self):
        self.original_file_set.next_file()
        new_filename = self.original_file_set.get_current_filename()
        self.translated_file_set.jump_to_file_by_name(new_filename)
        self._update_both_files()

    def jump_to_file_by_name(self, filename):
        file_exist = self.original_file_set.jump_to_file_by_name(filename)
        if file_exist:
            self.translated_file_set.jump_to_file_by_name(filename)
            self._update_both_files()
            return True
        else:
            return False
        
    def _update_original_file(self):
        self.original_json.clear()
        file_path = self.original_file_set.get_current_file_path()
        if file_path:
            self.original_json.parse(file_path)

    def _update_translated_file(self):
        self.translated_json.clear()
        file_path = self.translated_file_set.get_current_file_path()
        if file_path:
            self.translated_json.parse(file_path)
            self._update_translated_entry()
    
    def _update_both_files(self):
        self._update_original_file()
        self._update_translated_file()
# endregion

# region Entry
    def _update_translated_entry(self):
        current_id = self.get_current_entry_id()
        if current_id:
            index = self.translated_json.find_index_by_id(current_id)
            self.translated_json.set_current_index(index)

    def get_current_entry_id(self):
        return self.original_json.get_current_entry_id()

    def prev_entry(self):
        self.original_json.prev_entry()
        self._update_translated_entry()

    def next_entry(self):
        self.original_json.next_entry()
        self._update_translated_entry()

    def jump_to_index_by_id(self, id):
        index = self.original_json.find_index_by_id(id)
        if index >= 0:
            self.original_json.set_current_index(index)
            self._update_translated_entry()

    def get_original_entry(self):
        return self.original_json.get_entry()
    
    def get_translated_entry(self):
        return self.translated_json.get_entry()
    
    def get_current_index(self):
        return self.original_json.get_current_index()

    def get_entry_count(self):
        return self.original_json.get_entry_count()
        
# endregion