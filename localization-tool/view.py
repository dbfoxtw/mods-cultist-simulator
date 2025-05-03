import tkinter as tk
from tkinter import filedialog, scrolledtext

class MainView:
    def __init__(self, root, presenter):
        self.presenter = presenter
        self.root = root
        root.title("密教模擬器潤稿工具")

        # === 資料夾欄位 ===
        self.english_folder_entry = self._folder_row(0, "英文資料夾", self.presenter.on_browse_english)
        self.chinese_folder_entry = self._folder_row(1, "中文資料夾", self.presenter.on_browse_chinese)

        # === JSON 顯示區 ===
        self.original_json = self._text_area(2, "原文 JSON", 5, state="disabled")
        self.translated_json = self._text_area(3, "翻譯 JSON", 5, state="disabled")
        self.chatgpt_response = self._text_area(4, "CHATGPT 回應", 10, state="disabled")
        self.question_box = self._text_area(5, "詢問", 3, state="normal")
        tk.Button(root, text="送出", command=self.presenter.on_submit_question).grid(row=6, column=2, sticky="e", padx=5, pady=(0, 10))

        # === 檔案操作列 ===
        self.file_entry = self._nav_row(7, "目前檔案", [
            ("上一個", self.presenter.on_prev_file),
            ("下一個", self.presenter.on_next_file),
            ("跳至", self.presenter.on_jump_file)
        ])

        self.id_entry = self._nav_row(8, "目前 ID", [
            ("上一個", self.presenter.on_prev_id),
            ("下一個", self.presenter.on_next_id),
            ("跳至", self.presenter.on_jump_id)
        ])

        self.count_label = tk.Label(root, text="當前筆數 / 總筆數：0 / 0")
        self.count_label.grid(row=9, column=2, sticky="e", padx=10)

        root.update_idletasks()
        root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")
        root.resizable(False, False)

    def _folder_row(self, row, label, browse_cmd):
        tk.Label(self.root, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(self.root, width=80, state="readonly")
        entry.grid(row=row, column=1, padx=5)
        tk.Button(self.root, text="瀏覽", command=browse_cmd).grid(row=row, column=2, padx=5)
        return entry

    def _text_area(self, row, label, height, state="normal"):
        tk.Label(self.root, text=label).grid(row=row, column=0, sticky="nw", padx=10, pady=5)
        text = scrolledtext.ScrolledText(self.root, height=height, width=100, state=state)
        text.grid(row=row, column=1, columnspan=2, padx=5, pady=(0, 10))
        return text

    def _nav_row(self, row, label, buttons):
        tk.Label(self.root, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=10)
        entry = tk.Entry(self.root, width=40, state="readonly")
        entry.grid(row=row, column=1, sticky="w", padx=5)
        frame = tk.Frame(self.root)
        frame.grid(row=row, column=2, sticky="w")
        for text, command in buttons:
            tk.Button(frame, text=text, command=command).pack(side="left", padx=2)
        return entry

    def set_folder_entry(self, entry_widget, path):
        entry_widget.config(state="normal")
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)
        entry_widget.config(state="readonly")

    def set_entry_text(self, entry_widget, text):
        entry_widget.config(state="normal")
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, text)
        entry_widget.config(state="readonly")

    def set_text(self, text_widget, text):
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, text)
        text_widget.config(state="disabled")

    def get_question(self):
        return self.question_box.get("1.0", tk.END).strip()

    def set_count_label(self, current, total):
        self.count_label.config(text=f"當前筆數 / 總筆數：{current} / {total}")
