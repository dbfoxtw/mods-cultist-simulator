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

    def on_chatgpt_mode_changed(self):
        mode = self.view.get_chatgpt_mode()
        if mode == "web":
            self.view.set_chatgpt_mode_web()
        elif mode == "api":
            self.view.set_chatgpt_mode_api()

    def load_app_settings(self):
        self.app_settings.load_settings()
        self._update_original_folder(self.app_settings.original_folder_path)
        self._update_translated_folder(self.app_settings.translated_folder_path)

    def _update_original_folder(self, path):
        self.model.set_original_folder(path)
        self.view.set_original_folder(path)
        self._update_filename()
        self._update_original_json()

    def _update_translated_folder(self, path):
        self.model.set_translated_folder(path)
        self.view.set_translated_folder(path)
        self._update_tranlated_json()

    def on_browse_original(self):
        path = self.view.ask_directory(self.app_settings.original_folder_path)
        if path:
            self._update_original_folder(path)
            self.app_settings.original_folder_path = path
            self.app_settings.save_settings()

    def on_browse_translated(self):
        path = self.view.ask_directory(self.app_settings.translated_folder_path)
        if path:
            self._update_translated_folder(path)
            self.app_settings.translated_folder_path = path
            self.app_settings.save_settings()

    def on_submit_review(self):
        source_text = self.model.get_original_entry()
        translated_text = self.view.get_translated_json()

        if source_text and translated_text:
            response = self.chatgpt.review(source_text, translated_text)
            self.view.set_chatgpt_response(response)
        else:
            response = "有字串是空的，發送失敗"
            self.view.set_chatgpt_response(response)

    # Not used
    def on_reload_file(self):
        self.model.reload_file()
        self._update_both_json()

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
        json = self.model.get_original_entry()

        if not self.model.is_original_parsed():
            id = "讀取失敗"
            json = "讀取失敗"
        else:
            if not id.strip():
                id = "無內容"
            if not json.strip():
                json = "無內容"

        self.view.set_json_id(id)
        self.view.set_original_json(json)

        current_index = self.model.get_current_index()
        entry_count = self.model.get_entry_count()
        if entry_count > 0:
            self.view.set_count_label(current_index + 1, entry_count)
        else:
            self.view.set_count_label(0, 0)

    def _update_tranlated_json(self):
        json = self.model.get_translated_entry()

        if not self.model.is_translated_parsed():
            json = "讀取失敗"
        elif not json.strip():
            json = "無內容"

        self.view.set_translated_json(json)

    def _update_both_json(self):
        self._update_original_json()
        self._update_tranlated_json()

    # Not used
    def on_common_command(self):
        command = """你是神祕學卡牌遊戲翻譯審稿員，我會貼兩個文本，分別是英文原文、中文翻譯，請針對翻譯檢查以下問題：
1. 漏譯或誤譯（與英文原文不符）
2. 語病或句法錯誤
3. 不符合台灣慣用語的人名、地名、表達（如直翻、陸式用語）

此外，請遵守以下規定：
1. 保留引號用法。
2. 如果有提供，則保留專有詞。
3. 除了建議與理由，也需提供修正後的全文。
4. 若無問題只需回覆「無需修改」。"""
        self.view.set_clipboard_string(command)
        self.view.show_toast("已複製到剪貼簿")

    def on_translate_command(self):
        original = self.model.get_original_entry()
        translated = self.model.get_translated_entry()
        matched_nouns = self.app_settings.extract_proper_nouns_from_text(translated)

        if matched_nouns:
            proper_noun_text = "\n".join(matched_nouns)
        else:
            proper_noun_text = "無"

        command = f"""英文：
{original}

中文：
{translated}

專有詞：
{proper_noun_text}"""
        self.view.set_clipboard_string(command)
        self.view.show_toast("已複製到剪貼簿")

    def on_add_proper_noun(self):
        word = self.view.get_proper_entry().strip()
        if word:
            self.app_settings.add_proper_noun(word)
            self.view.show_toast(f"已新增：{word}")
            if self.view.is_proper_noun_window_open():
                self.view.show_proper_noun_list(self.app_settings.get_proper_nouns())

    def on_remove_proper_noun(self):
        word = self.view.get_proper_entry().strip()
        if word:
            self.app_settings.remove_proper_noun(word)
            self.view.show_toast(f"已刪除：{word}")
            if self.view.is_proper_noun_window_open():
                self.view.show_proper_noun_list(self.app_settings.get_proper_nouns())

    def on_show_proper_noun_list(self):
        nouns = self.app_settings.get_proper_nouns()
        self.view.show_proper_noun_list(nouns)