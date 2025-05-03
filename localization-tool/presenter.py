import os
from model import MainModel

class MainPresenter:
    def __init__(self, model: MainModel, view):
        self.model = model
        self.view = view

    def on_browse_english(self):
        path = self._ask_directory()
        if path:
            self.model.set_english_folder(path)
            self.view.set_folder_entry(self.view.english_folder_entry, path)
            self.refresh_view()

    def on_browse_chinese(self):
        path = self._ask_directory()
        if path:
            self.model.set_chinese_folder(path)
            self.view.set_folder_entry(self.view.chinese_folder_entry, path)

    def on_submit_question(self):
        question = self.view.get_question()
        print("送出詢問：", question)
        # 實際可在這裡加上 ChatGPT 呼叫邏輯

    def on_prev_file(self):
        self.model.prev_file()
        self.refresh_view()

    def on_next_file(self):
        self.model.next_file()
        self.refresh_view()

    def on_jump_file(self):
        # TODO: 實作跳至功能（目前省略）
        pass

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

        data = self.model.load_current_json()

        # 顯示 JSON 主體文字
        self.view.set_text(self.view.original_json, str(data))
        self.view.set_text(self.view.translated_json, "")  # 預留翻譯處
        self.view.set_text(self.view.chatgpt_response, "")
        self.view.set_count_label(self.model.current_file_index + 1, self.model.get_total_files())

    def _ask_directory(self):
        from tkinter import filedialog
        return filedialog.askdirectory()
