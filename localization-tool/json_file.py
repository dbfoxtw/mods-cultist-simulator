import copy
import json5

class JsonFile:
    def __init__(self):
        self.clear()

    def clear(self):
        self._filtered_data = []
        self._current_index = 0

    def parse(self, path):
        self.clear()

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json5.load(f)

            # 確認只有一個 top-level key
            if len(data) != 1:
                raise ValueError("JSON 應只有一個 top-level key")

            root_key = next(iter(data))
            original_array = data[root_key]

            # 過濾後資料
            self._filtered_data = [self._filter_entry(entry) for entry in original_array]

        except json5.JSONDecodeError as e:
            print("JSON5 解析錯誤")
            print(f"行：{e.lineno}, 欄：{e.colno}, 錯誤：{e.msg}")
        except Exception as e:
            print(f"其他錯誤：{e}")

    def _filter_entry(self, entry):
        base = {
            k: entry[k]
            for k in ("id", "label", "startdescription", "descriptionunlocked")
            if k in entry
        }
        if "drawmessages" in entry:
            base["drawmessages"] = entry["drawmessages"]
        return base
    
    def prev_entry(self):
        if self._current_index > 0:
            self._current_index -= 1

    def next_entry(self):
        if self._current_index < len(self._filtered_data) - 1:
            self._current_index += 1

    def find_entry(self, id_value):
        found_index = None
        for i, entry in enumerate(self._filtered_data):
            if entry.get("id") == id_value:
                found_index = i
                break

        if found_index is not None:
            self._current_index = found_index
        else:
            self._current_index = -1

    def get_entry_content(self):
        data = self._filtered_data[self._current_index]
        data = json5.dumps(data, ensure_ascii=False, indent=4)
        return data
    
    def get_current_entry_id(self):
        data = self._filtered_data[self._current_index]
        if data:
            return data.get("id")
        else:
            return ""
    
    def get_current_index(self):
        return self._current_index

    def get_entry_count(self):
        return len(self._filtered_data)