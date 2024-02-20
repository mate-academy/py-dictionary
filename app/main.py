from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = (2 / 3)
        self.table = [None] * self.capacity
        self.size = 0

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.table[index] and self.table[index][0] != key:
            index = (index + 1) % self.capacity
        return index

    def resize(self) -> None:
        self.capacity *= 2
        old_table = self.table
        self.table = [None] * self.capacity
        self.size = 0
        for item in old_table:
            if item is not None:
                self[item[0]] = item[2]

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key=key)
        if not self.table[index]:
            raise KeyError(f"{key} not found !")
        return self.table[index][2]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)
        if not self.table[index]:
            if self.capacity * self.load_factor < self.size:
                self.resize()
                index = self.get_index(key)
            self.size += 1
        self.table[index] = (key, hash(key), value)

    def __len__(self) -> int:
        return self.size
