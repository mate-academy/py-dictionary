from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.load_factor = 2 / 3

    def find_index(self, key: Hashable) -> int | None:
        index_element = hash(key) % len(self.hash_table)
        count = 0

        while count < len(self.hash_table):
            if isinstance(self.hash_table[index_element], tuple) \
                    and self.hash_table[index_element][0] == key:
                return index_element

            index_element += 1
            index_element %= len(self.hash_table)
            count += 1

    def resize_hash_table(self) -> bool:
        if self.length >= int(len(self.hash_table) * self.load_factor):
            self.hash_table += [None] * len(self.hash_table)

            return True
        return False

    def reindex_element_after_resize_table(self) -> None:
        elements_before_resize = [
            element
            for element in self.hash_table
            if isinstance(element, tuple)
        ]
        self.hash_table = [None] * len(self.hash_table)

        for key, value in elements_before_resize:
            self.insert_element_in_hash_table(key=key, value=value)

    def insert_element_in_hash_table(self, key: Hashable, value: Any) -> None:
        index_key = hash(key) % len(self.hash_table)

        while True:
            if self.hash_table[index_key] is None:
                self.hash_table[index_key] = (key, value)
                break
            elif index_key == (len(self.hash_table) - 1) \
                    and self.hash_table[index_key] is not None:
                index_key = 0
            else:
                index_key += 1

    def __setitem__(self, key: Hashable, value: Any) -> None:
        for element in self.hash_table:
            if isinstance(element, tuple) and (element[0] == key):
                index_el = self.hash_table.index(element)
                self.hash_table[index_el] = (key, value)
                return

        self.insert_element_in_hash_table(key=key, value=value)
        self.length += 1

        check_resize = self.resize_hash_table()
        if check_resize:
            self.reindex_element_after_resize_table()

    def __getitem__(self, item: Any) -> Any | Exception:
        index_element = self.find_index(key=item)

        if index_element is not None:
            return self.hash_table[index_element][1]
        else:
            raise KeyError

    def __delitem__(self, key: Hashable) -> None:
        index_element = self.find_index(key=key)

        if index_element is not None:
            self.hash_table[index_element] = None
            self.length -= 1

    def __len__(self) -> int:
        return self.length
