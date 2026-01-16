from typing import Any


class Dictionary:

    def __init__(self, initial_size: int = 8) -> None:
        self.size = initial_size
        self.count = 0
        self.table = [None] * initial_size

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.size

        while True:
            element = self.table[index]
            if element is None:
                raise KeyError(key)
            stored_key, stored_hash, stored_value = element
            if stored_hash == key_hash and stored_key == key:
                return stored_value
            index = (index + 1) % self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.count + 1) > self.size * (2 / 3):
            self._resize()
        key_hash = hash(key)
        index = key_hash % self.size
        while True:
            element = self.table[index]
            if element is None:
                self.table[index] = (key, key_hash, value)
                self.count += 1
                return
            stored_key, stored_hash, stored_value = element
            if stored_hash == key_hash and stored_key == key:
                self.table[index] = (key, key_hash, value)
                return
            index = (index + 1) % self.size

    def _resize(self) -> None:
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.count = 0
        for element in old_table:
            if element is not None:
                stored_key, stored_hash, stored_value = element
                self[stored_key] = stored_value
