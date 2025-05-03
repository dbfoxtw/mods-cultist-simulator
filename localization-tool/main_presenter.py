import os
from main_model import MainModel
from main_view import MainView
from app_settings import AppSettings

class MainPresenter:
    def __init__(self, model: MainModel, view: MainView):
        self.app_settings = AppSettings()
        self.model = model
        self.view = view

    def load_app_settings(self):
        self.app_settings.load_settings()
        self._update_english_folder(self.app_settings.english_folder_path)
        self._update_chinese_folder(self.app_settings.chinese_folder_path)
        self.refresh_view()

    def _update_english_folder(self, path):
        self.model.set_english_folder(path)
        self.view.set_english_folder(path)

    def _update_chinese_folder(self, path):
        self.model.set_chinese_folder(path)
        self.view.set_chinese_folder(path)

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
            self.refresh_view();

    def on_submit_question(self):
        question = self.view.get_question()
        print("送出詢問：", question)
        # 實際可在這裡加上 ChatGPT 呼叫邏輯

    def on_prev_file(self):
        if self.model.is_first_file():
            self.view.show_first_file_warning()
        else:
            self.model.prev_file()
            self.refresh_view()

    def on_next_file(self):
        if self.model.is_last_file():
            self.view.show_last_file_warning()
        else:
            self.model.next_file()
            self.refresh_view()

    def on_jump_file(self):
        filename = self.view.prompt_filename()
        self.model.jump_to_file_by_name(filename)
        self.refresh_view()

    def on_prev_id(self):
        # TODO: 實作上一個 ID
        pass

    def on_next_id(self):
        # TODO: 實作下一個 ID
        pass

    def on_jump_id(self):
        # TODO: 實作跳至 ID
        pass

    def refresh_view(self):
        filename = self.model.get_current_filename()
        self.view.set_entry_text(self.view.file_entry, filename)

        # data = self.model.load_current_json()

        # 顯示 JSON 主體文字
        # self.view.set_text(self.view.original_json, str(data))
        # self.view.set_text(self.view.translated_json, "")  # 預留翻譯處
        # self.view.set_text(self.view.chatgpt_response, "")
        # self.view.set_count_label(self.model.current_file_index + 1, self.model.get_total_files())

