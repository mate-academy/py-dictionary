from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.load_factor = round(2 / 3, 2)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > len(self.hash_table) * self.load_factor:
            self.resize()
        hash_index = hash(key) % len(self.hash_table)
        values = [key, hash(key), value]
        while True:
            if (
                    self.hash_table[hash_index] is not None
                    and self.hash_table[hash_index][0] == key
                    and self.hash_table[hash_index][1] == hash(key)
            ):
                self.hash_table[hash_index] = values
                break
            elif self.hash_table[hash_index] is None:
                self.length += 1
                self.hash_table[hash_index] = values
                break
            hash_index = (hash_index + 1) % len(self.hash_table)

    def __getitem__(self, key: Hashable) -> Any:
        hash_index = hash(key) % len(self.hash_table)
        while True:
            if self.hash_table[hash_index] is None:
                raise KeyError(key)
            if self.hash_table[hash_index][0] == key:
                return self.hash_table[hash_index][2]
            hash_index = (hash_index + 1) % len(self.hash_table)

    def resize(self) -> None:
        current_hash_table = self.hash_table
        self.hash_table = [None] * 2 * len(current_hash_table)
        self.length = 0
        for item in current_hash_table:
            if item is not None:
                self[item[0]] = item[2]

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        hash_index = hash(key) % len(self.hash_table)
        while True:
            if self.hash_table[hash_index][0] == key:
                self.hash_table[hash_index] = None
                self.length -= 1
                break
            hash_index = (hash_index + 1) % len(self.hash_table)

    def get(self, key: Hashable = None) -> Any:
        for item in self.hash_table:
            if item is not None and item[0] == key:
                return item[2]
        return key

    def pop(self, key: Hashable) -> Any:
        for index, item in enumerate(self.hash_table):
            if item is not None and item[0] == key:
                current_item = item
                self.hash_table[index] = None
                self.length -= 1
                return current_item[2]
        raise KeyError(key)
