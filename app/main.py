from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.table: list[Any] = [None] * 5
        self.size: int = 0

    def resize(self) -> None:
        old_table = self.table

        self.table = [None] * (len(old_table) * 2)

        old_size = self.size
        self.size = 0

        for bucket in old_table:
            if bucket is not None:
                for key, key_hash, value in bucket:
                    self[key] = value

        self.size = old_size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / len(self.table) > 0.7:
            self.resize()

        key_hash = hash(key)
        index = key_hash % len(self.table)

        if self.table[index] is None:
            self.table[index] = []

        for pair in self.table[index]:
            if pair[0] == key:
                pair[2] = value
                return

        self.table[index].append([key, key_hash, value])
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % len(self.table)

        if self.table[index] is None:
            raise KeyError(f"Key '{key}' not found in dictionary")

        for pair in self.table[index]:
            if pair[0] == key:
                return pair[2]

        raise KeyError(f"Key '{key}' not found in dictionary")

    def __len__(self) -> int:
        return self.size
