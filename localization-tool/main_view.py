import customtkinter as ctk
from tkinter import messagebox

class MainView:
    def __init__(self, root, presenter):
        self.default_font = ("微軟正黑體", 14)
        self.presenter = presenter
        self.root = root
        root.title("密教模擬器潤稿工具")

        # === 資料夾欄位 ===
        self.english_folder_entry = self._folder_row(0, "英文資料夾", self.presenter.on_browse_english)
        self.chinese_folder_entry = self._folder_row(1, "中文資料夾", self.presenter.on_browse_chinese)

        # === 檔案操作列 ===
        self.file_entry = self._nav_row(2, "目前檔案", [
            ("跳至", self.presenter.on_jump_file),
            ("上一個", self.presenter.on_prev_file),
            ("下一個", self.presenter.on_next_file),
            ("重新讀取", self.presenter.on_reload_file)
        ])

        # === ID操作列 ===
        self.id_entry = self._nav_row(3, "目前 ID", [
            ("跳至", self.presenter.on_jump_id),
            ("上一個", self.presenter.on_prev_id),
            ("下一個", self.presenter.on_next_id)
        ])

        self.original_json = self._text_area(4, "原文", 10)
        self.translated_json = self._text_area(5, "翻譯 / 修訂", 10)
        self.chatgpt_response = self._text_area(6, "CHATGPT 回應", 15)
        
        footer_frame = ctk.CTkFrame(self.root)
        footer_frame.grid(row=7, column=2, sticky="e")
        self.count_label = ctk.CTkLabel(footer_frame, text="當前筆數 / 總筆數：0 / 0")
        self.count_label.pack(side="left", padx=2)
        ctk.CTkButton(footer_frame, text="審稿", command=self.presenter.on_submit_review, width=70).pack(side="left", padx=8)

        root.geometry("1030x930")
        root.resizable(True, True)

    def _folder_row(self, row, label, browse_cmd):
        ctk.CTkLabel(self.root, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = ctk.CTkEntry(self.root, width=600)
        entry.configure(state="disabled")
        entry.grid(row=row, column=1, padx=5)
        ctk.CTkButton(self.root, text="瀏覽", command=browse_cmd, width=70).grid(row=row, column=2, padx=5)
        return entry

    def _text_area(self, row, label, height):
        ctk.CTkLabel(self.root, text=label).grid(row=row, column=0, sticky="nw", padx=10, pady=5)
        textbox = ctk.CTkTextbox(self.root, height=height*20, width=800, font=self.default_font, undo=True)
        textbox.configure(state="disabled")
        textbox.grid(row=row, column=1, columnspan=2, padx=5, pady=(0, 10))
        return textbox

    def _nav_row(self, row, label, buttons):
        ctk.CTkLabel(self.root, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = ctk.CTkEntry(self.root, width=400)
        entry.configure(state="disabled")
        entry.grid(row=row, column=1, sticky="w", padx=5)
        frame = ctk.CTkFrame(self.root)
        frame.grid(row=row, column=2, sticky="w")
        for text, command in buttons:
            ctk.CTkButton(frame, text=text, command=command, width=70).pack(side="left", padx=2)
        return entry

    def _set_folder_entry(self, entry_widget, path):
        entry_widget.configure(state="normal")
        entry_widget.delete(0, 'end')
        entry_widget.insert(0, path)
        entry_widget.configure(state="disabled")

    def _set_entry_text(self, entry_widget, text):
        entry_widget.configure(state="normal")
        entry_widget.delete(0, 'end')
        entry_widget.insert(0, text)
        entry_widget.configure(state="disabled")

    def _set_text(self, text_widget, text, readonly):
        text_widget.configure(state="normal")
        text_widget.delete("1.0", 'end')
        text_widget.insert('end', text)
        if readonly:
            text_widget.configure(state="disabled")

    def set_english_folder(self, path):
        self._set_folder_entry(self.english_folder_entry, path)

    def set_chinese_folder(self, path):
        self._set_folder_entry(self.chinese_folder_entry, path)

    def set_filename(self, filename):
        self._set_entry_text(self.file_entry, filename)

    def set_json_id(self, id):
        self._set_entry_text(self.id_entry, id)

    def set_original_json(self, json):
        self._set_text(self.original_json, json, True)

    def set_translated_json(self, json):
        self._set_text(self.translated_json, json, False)

    def get_translated_json(self):
        return self.translated_json.get("1.0", "end").strip()

    def set_chatgpt_response(self, response):
        self._set_text(self.chatgpt_response, response, True)

    def set_count_label(self, current, total):
        self.count_label.configure(text=f"當前筆數 / 總筆數：{current} / {total}")

    def ask_directory(self, path):
        return ctk.filedialog.askdirectory(initialdir=path)

    def prompt_filename(self):
        dialog = ctk.CTkInputDialog(title="跳至檔案", text="請輸入檔案名稱（包含 .json）：")
        return dialog.get_input()

    def prompt_json_id(self):
        dialog = ctk.CTkInputDialog(title="跳至檔案", text="請輸入JSON ID：")
        return dialog.get_input()

    def show_first_file_warning(self):
        messagebox.showwarning("警告", "已經是第一個檔案")

    def show_last_file_warning(self):
        messagebox.showwarning("警告", "已經是最後一個檔案")

    def show_file_not_found_error(self, filename):
        messagebox.showerror("錯誤", f"找不到檔案 {filename}")
