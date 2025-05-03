import os
from main_model import MainModel
from main_view import MainView
from app_settings import AppSettings
from chatgpt_helper import ChatGPTHelper

class MainPresenter:
    def __init__(self, model: MainModel, view: MainView):
        self.app_settings = AppSettings()
        self.model = model
        self.view = view
        self.chatgpt = ChatGPTHelper()

    def load_app_settings(self):
        self.app_settings.load_settings()
        self._update_english_folder(self.app_settings.english_folder_path)
        self._update_chinese_folder(self.app_settings.chinese_folder_path)

    def _update_english_folder(self, path):
        self.model.set_english_folder(path)
        self.view.set_english_folder(path)
        self._update_filename()
        self._update_original_json()

    def _update_chinese_folder(self, path):
        self.model.set_chinese_folder(path)
        self.view.set_chinese_folder(path)
        self._update_tranlated_json()

    def on_browse_english(self):
        path = self.view.ask_directory(self.app_settings.english_folder_path)
        if path:
            self._update_english_folder(path)
            self.app_settings.english_folder_path = path
            self.app_settings.save_settings()

    def on_browse_chinese(self):
        path = self.view.ask_directory(self.app_settings.chinese_folder_path)
        if path:
            self._update_chinese_folder(path)
            self.app_settings.chinese_folder_path = path
            self.app_settings.save_settings()

    def on_submit_review(self):
        source_text = self.model.get_english_entry()
        translated_text = self.model.get_chinese_entry()

        if source_text and translated_text:
            response = self.chatgpt.review(source_text, translated_text)
            self.view.set_chatgpt_response(response)
        else:
            response = "有字串是空的，發送失敗"
            self.view.set_chatgpt_response(response)

    def on_prev_file(self):
        if self.model.is_first_file():
            self.view.show_first_file_warning()
        else:
            self.model.prev_file()
            self._update_filename()
            self._update_both_json()

    def on_next_file(self):
        if self.model.is_last_file():
            self.view.show_last_file_warning()
        else:
            self.model.next_file()
            self._update_filename()
            self._update_both_json()

    def on_jump_file(self):
        filename = self.view.prompt_filename()
        if filename:
            self.model.jump_to_file_by_name(filename)
            self._update_filename()
            self._update_both_json()

    def on_prev_id(self):
        self.model.prev_entry()
        self._update_both_json()

    def on_next_id(self):
        self.model.next_entry()
        self._update_both_json()

    def on_jump_id(self):
        id = self.view.prompt_json_id()
        if id:
            self.model.jump_to_index_by_id(id)
            self._update_both_json()

    def _update_filename(self):
        filename = self.model.get_current_filename()
        self.view.set_filename(filename)

    def _update_original_json(self):
        id = self.model.get_current_entry_id()
        json = self.model.get_english_entry()
        self.view.set_json_id(id)
        self.view.set_original_json(json)

        current_index = self.model.get_current_index()
        entry_count = self.model.get_entry_count()
        if entry_count > 0:
            self.view.set_count_label(current_index + 1, entry_count)
        else:
            self.view.set_count_label(0, 0)

    def _update_tranlated_json(self):
        json = self.model.get_chinese_entry()
        self.view.set_translated_json(json)

    def _update_both_json(self):
        self._update_original_json()
        self._update_tranlated_json()