from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.load_factor = 0.75

    def __len__(self) -> int:
        return self.length

    def _hash(self, key: Hashable) -> int:
        return hash(key) % len(self.hash_table)

    def __setitem__(self, key: Any, value: Any) -> None:
        index: int = self._hash(key)

        if self.hash_table[index] is None:
            self.hash_table[index] = []

        for hash_index, (hash_key, _) in enumerate(self.hash_table[index]):
            if hash_key == key:
                self.hash_table[index][hash_index] = (key, value)
                return
        self.hash_table[index].append((key, value))
        self.length += 1

        if self.length / len(self.hash_table) > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index: int = self._hash(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} not found")

        for k, v in self.hash_table[index]:
            if k == key:
                return v

        raise KeyError(f"Key {key} not found")

    def _resize(self) -> None:
        new_capacity = len(self.hash_table) * 2
        new_table: list = [None] * new_capacity

        old_table = self.hash_table
        self.hash_table = new_table
        self.length = 0

        for bucket in old_table:
            if bucket:
                for key, value in bucket:
                    self[key] = value
