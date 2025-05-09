import json

class JsonFile:
    def __init__(self):
        self.clear()

    def clear(self):
        self._entries = []
        self._current_index = 0

    def parse(self, path, filtered=True):
        self.clear()

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if len(data) != 1:
                raise ValueError("JSON 應只有一個 top-level key")

            root_key = next(iter(data))
            original_array = data[root_key]

            if filtered:
                self._entries = [self._filter_entry(entry) for entry in original_array]
            else:
                self._entries = original_array

        except json.JSONDecodeError as e:
            print("json 解析錯誤")
            print(f"行：{e.lineno}, 欄：{e.colno}, 錯誤：{e.msg}")
        except Exception as e:
            print(f"其他錯誤：{e}")

    # 1. 如果key是drawmessages，保留原內容
    # 2. 若不是，則檢查每一層，key保留"id", "label", "description", "startdescription", "descriptionunlocked"
    # 3. 如果該層key只剩下"id"，或無內容，則去掉
    def _filter_entry(self, entry):
        def recursive_filter(obj):
            if isinstance(obj, dict):
                if "drawmessages" in obj:
                    return {"drawmessages": obj["drawmessages"]}
                filtered = {}
                for k, v in obj.items():
                    if k in ("id", "label", "description", "startdescription", "descriptionunlocked"):
                        filtered[k] = v
                    elif isinstance(v, dict):
                        nested = recursive_filter(v)
                        if nested and (list(nested.keys()) != ["id"]):
                            filtered[k] = nested
                    elif isinstance(v, list):
                        nested_list = [recursive_filter(i) for i in v]
                        nested_list = [i for i in nested_list if isinstance(i, dict) and i and list(i.keys()) != ["id"]]
                        if nested_list:
                            filtered[k] = nested_list
                return filtered
            elif isinstance(obj, list):
                return [recursive_filter(i) for i in obj if isinstance(i, (dict, list))]
            else:
                return obj
        return recursive_filter(entry)
    
    def prev_entry(self):
        if self._current_index > 0:
            self._current_index -= 1

    def next_entry(self):
        if self._current_index < len(self._entries) - 1:
            self._current_index += 1

    def find_index_by_id(self, id_value):
        if not id_value:
            return -1

        found_index = None
        for i, entry in enumerate(self._entries):
            if entry.get("id") == id_value:
                found_index = i
                break

        if found_index is not None:
            return found_index
        else:
            return -1
        
    def set_current_index(self, index):
        self._current_index = index

    def get_entry(self):
        if self._current_index < 0 or self._current_index >= len(self._entries):
            return ""
        data = self._entries[self._current_index]
        data = json.dumps(data, ensure_ascii=False, indent=4)
        return data
    
    def get_current_entry_id(self):
        if self._current_index < 0 or self._current_index >= len(self._entries):
            return ""
        data = self._entries[self._current_index]
        if data:
            return data.get("id")
        else:
            return ""
    
    def get_current_index(self):
        return self._current_index

    def get_entry_count(self):
        return len(self._entries)