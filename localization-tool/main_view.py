import customtkinter as ctk
from tkinter import messagebox

class MainView:
    def __init__(self, root, presenter):
        self.default_font = ("微軟正黑體", 14)
        self.presenter = presenter
        self.root = root
        root.title("密教模擬器潤稿工具")
        root.grid_columnconfigure(1, weight=1)

        # === ChatGPT 功能選擇列 ===
        self.chatgpt_mode = ctk.StringVar(value="web")  # 預設為網頁

        ctk.CTkLabel(root, text="ChatGPT功能").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        mode_frame = ctk.CTkFrame(root)
        mode_frame.grid(row=0, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        ctk.CTkRadioButton(mode_frame, text="網頁", variable=self.chatgpt_mode, value="web", command=self.presenter.on_chatgpt_mode_changed).pack(side="left")
        ctk.CTkRadioButton(mode_frame, text="API", variable=self.chatgpt_mode, value="api", command=self.presenter.on_chatgpt_mode_changed).pack(side="left", padx=5)

        # === 資料夾欄位 ===
        self.original_folder_entry = self._folder_row(1, "英文資料夾", self.presenter.on_browse_original)
        self.translated_folder_entry = self._folder_row(2, "中文資料夾", self.presenter.on_browse_translated)

        # === 檔案操作列 ===
        self.file_entry = self._nav_row(3, "目前檔案", [
            ("跳至", self.presenter.on_jump_file),
            ("上一個", self.presenter.on_prev_file),
            ("下一個", self.presenter.on_next_file),
        ])

        # === ID操作列 ===
        self.id_entry = self._nav_row(4, "目前 ID", [
            ("跳至", self.presenter.on_jump_id),
            ("上一個", self.presenter.on_prev_id),
            ("下一個", self.presenter.on_next_id)
        ])

        # === 專有名詞 ===
        ctk.CTkLabel(root, text="專有名詞").grid(row=5, column=0, sticky="w", padx=10, pady=5)

        _proper_noun_frame = ctk.CTkFrame(root)
        _proper_noun_frame.grid(row=5, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        ctk.CTkLabel(_proper_noun_frame, text="英文").pack(side="left")
        self._proper_noun_english_entry = ctk.CTkEntry(_proper_noun_frame, width=200)
        self._proper_noun_english_entry.pack(side="left", padx=(5, 0))

        ctk.CTkLabel(_proper_noun_frame, text="中文").pack(side="left", padx=(5, 0))
        self._proper_noun_chinese_entry = ctk.CTkEntry(_proper_noun_frame, width=200)
        self._proper_noun_chinese_entry.pack(side="left", padx=(5, 0))        

        ctk.CTkButton(_proper_noun_frame, text="新增", width=70, command=self.presenter.on_add_proper_noun).pack(side="left", padx=(5, 2))
        ctk.CTkButton(_proper_noun_frame, text="刪除", width=70, command=self.presenter.on_remove_proper_noun).pack(side="left", padx=2)
        ctk.CTkButton(_proper_noun_frame, text="列表", width=70, command=self.presenter.on_show_proper_noun_list).pack(side="left", padx=2)

        self.original_json = self._text_area(6, "原文", 10)
        self.translated_json = self._text_area(7, "翻譯 / 修訂", 10)

        self.proper_noun_window = None

        # === ChatGPT回應 ===
        self.chatgpt_response_label = ctk.CTkLabel(self.root, text="CHATGPT 回應")
        self.chatgpt_response_label.grid(row=8, column=0, sticky="nw", padx=10, pady=5)
        self.chatgpt_response = ctk.CTkTextbox(self.root, height=15 * 20, font=self.default_font, undo=True)
        self.chatgpt_response.configure(state="disabled")
        self.chatgpt_response.grid(row=8, column=1, columnspan=2, padx=(5, 10), pady=5, sticky="nsew")

        self.count_label = ctk.CTkLabel(self.root, text="當前筆數 / 總筆數：0 / 0")
        self.count_label.grid(row=9, column=1, sticky="w", padx=5, pady=5)

        footer_frame = ctk.CTkFrame(self.root)
        footer_frame.grid(row=9, column=2, sticky="e", padx=(0, 10))
        self.review_button = ctk.CTkButton(footer_frame, text="審稿", command=self.presenter.on_submit_review, width=70)
        self.review_button.pack(side="left")
        self.translate_cmd_button = ctk.CTkButton(footer_frame, text="複製指令", command=self.presenter.on_translate_command, width=90)
        self.translate_cmd_button.pack(side="left")

        self.set_chatgpt_mode_web()

        root.resizable(False, False)

    def _folder_row(self, row, label, browse_cmd):
        ctk.CTkLabel(self.root, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        
        frame = ctk.CTkFrame(self.root)
        frame.grid(row=row, column=1, columnspan=2, sticky="nsew", padx=(5, 10), pady=5)
        frame.grid_columnconfigure(0, weight=1)

        entry = ctk.CTkEntry(frame)
        entry.configure(state="disabled")
        entry.grid(row=0, column=0, sticky="nsew")

        button = ctk.CTkButton(frame, text="瀏覽", command=browse_cmd, width=70)
        button.grid(row=0, column=1, padx=(5, 0), sticky="e")
        return entry

    def _nav_row(self, row, label, buttons):
        ctk.CTkLabel(self.root, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)

        row_frame = ctk.CTkFrame(self.root)
        row_frame.grid(row=row, column=1, columnspan=2, sticky="nsew", padx=(5, 10), pady=5)
        row_frame.grid_columnconfigure(0, weight=1)

        entry = ctk.CTkEntry(row_frame)
        entry.configure(state="disabled")
        entry.grid(row=0, column=0, sticky="nsew")
        
        button_frame = ctk.CTkFrame(row_frame)
        button_frame.grid(row=0, column=1, padx=(5, 0), sticky="e")
        
        for i, (text, command) in enumerate(buttons):
            if i == 0:
                ctk.CTkButton(button_frame, text=text, command=command, width=70).pack(side="left")
            else:
                ctk.CTkButton(button_frame, text=text, command=command, width=70).pack(side="left", padx=(4, 0))

        return entry

    def _text_area(self, row, label, height):
        ctk.CTkLabel(self.root, text=label).grid(row=row, column=0, sticky="nw", padx=10, pady=5)
        textbox = ctk.CTkTextbox(self.root, height=height*20, font=self.default_font, undo=True)
        textbox.configure(state="disabled")
        textbox.grid(row=row, column=1, columnspan=2, padx=(5, 10), pady=5, sticky="nsew")
        return textbox

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

    def get_chatgpt_mode(self):
        return self.chatgpt_mode.get()
    
    def set_chatgpt_mode_web(self):
        self.chatgpt_response_label.grid_remove()
        self.chatgpt_response.grid_remove()
        self.review_button.pack_forget()
        self.translate_cmd_button.pack(side="left")
        self.root.geometry("1050x700")

    def set_chatgpt_mode_api(self):
        self.chatgpt_response_label.grid()
        self.chatgpt_response.grid()
        self.translate_cmd_button.pack_forget()
        self.review_button.pack(side="left")
        self.root.geometry("1030x1000")

    def set_original_folder(self, path):
        self._set_folder_entry(self.original_folder_entry, path)

    def set_translated_folder(self, path):
        self._set_folder_entry(self.translated_folder_entry, path)

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

    def set_clipboard_string(self, str):
        self.root.clipboard_clear()
        self.root.clipboard_append(str)
        self.root.update()

    def show_toast(self, message, duration=1500):
        toast = ctk.CTkToplevel(self.root)
        toast.overrideredirect(True)  # 去掉邊框
        toast.attributes("-topmost", True)  # 永遠在最上面

        label = ctk.CTkLabel(toast, text=message, corner_radius=10, fg_color="#333333", text_color="white")
        label.pack(padx=10, pady=5)

        # 定位：畫面右下角
        self.root.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() - 200
        y = self.root.winfo_y() + self.root.winfo_height() - 100
        toast.geometry(f"+{x}+{y}")

        # 設定自動關閉
        toast.after(duration, toast.destroy)

    def get_proper_noun_english_entry(self):
        return self._proper_noun_english_entry.get()
    
    def get_proper_noun_chinese_entry(self):
        return self._proper_noun_chinese_entry.get()
    
    def is_proper_noun_window_exist(self):
        return self.proper_noun_window and self.proper_noun_window.winfo_exists()

    def show_proper_noun_table(self, proper_nouns):
        if self.proper_noun_window and self.proper_noun_window.winfo_exists():
            self._update_proper_noun_table(proper_nouns)
            return

        self.proper_noun_window = ctk.CTkToplevel(self.root)
        self.proper_noun_window.title("專有名詞列表")
        self.proper_noun_window.geometry("400x500")
        self.proper_noun_window.resizable(False, False)

        self.proper_noun_window.transient(self.root)
        self.proper_noun_window.lift()

        self._table_scroll_frame = ctk.CTkScrollableFrame(self.proper_noun_window)
        self._table_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self._update_proper_noun_table(proper_nouns)

    def _update_proper_noun_table(self, proper_nouns):
        for widget in self._table_scroll_frame.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self._table_scroll_frame)
        header.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(header, text="英文", width=180, anchor="w").pack(side="left", padx=(10, 5))
        ctk.CTkLabel(header, text="中文", width=180, anchor="w").pack(side="left")

        for pn in proper_nouns:
            row = ctk.CTkFrame(self._table_scroll_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=pn.english, width=180, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=pn.chinese, width=180, anchor="w").pack(side="left")