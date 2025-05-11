import csv
from dataclasses import dataclass
from typing import List

@dataclass
class ProperNoun:
    english: str
    chinese: str

class ProperNounManager:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.cache: List[ProperNoun] = []
        self._load_cache()

    def _load_cache(self):
        try:
            with open(self.csv_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                self.cache = [ProperNoun(eng, chi) for eng, chi in reader if eng and chi]
        except FileNotFoundError:
            self.cache = []

    def _save_cache(self):
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for pn in self.cache:
                writer.writerow([pn.english, pn.chinese])

    def add(self, english: str, chinese: str) -> bool:
        english_lower = english.lower()
        if any(pn.english.lower() == english_lower and pn.chinese == chinese for pn in self.cache):
            return False
        self.cache.append(ProperNoun(english, chinese))
        self._save_cache()
        return True

    def delete(self, english: str = None, chinese: str = None) -> int:
        original_len = len(self.cache)

        if english:
            english = english.lower()

        def match(pn: ProperNoun):
            if english and chinese:
                return pn.english.lower() == english and pn.chinese == chinese
            elif english:
                return pn.english.lower() == english
            elif chinese:
                return pn.chinese == chinese
            return False

        self.cache = [pn for pn in self.cache if not match(pn)]
        deleted_count = original_len - len(self.cache)

        if deleted_count > 0:
            self._save_cache()
        return deleted_count

    def search_in_text(self, text: str) -> List[ProperNoun]:
        return [pn for pn in self.cache if pn.chinese in text]

    def list_all(self) -> List[ProperNoun]:
        return sorted(self.cache, key=lambda pn: pn.english.lower())
