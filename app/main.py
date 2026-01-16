from typing import Any, Hashable, Optional


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.capacity = 8

    def get_index_from_hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if self.length >= self.capacity * (2 / 3):
            self.resize()
        index = hash(key) % self.capacity
        while True:
            if not self.hash_table[index]:
                self.length += 1
            if not self.hash_table[index] or self.hash_table[index][0] == key:
                self.hash_table[index] = (key, hash(key), value)
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        return self.get(key)

    def get_index(self, key: Hashable) -> int:
        start_index = hash(key) % self.capacity
        index = start_index
        while True:
            if self.hash_table[index] and self.hash_table[index][0] == key:
                return index
            index = (index + 1) % self.capacity
            if index == start_index:
                raise KeyError("Key was not found")

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        if self.get_index(key) is not None:
            return self.hash_table[self.get_index(key)][2]
        return default

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)
        self.hash_table[index] = None
        self.length -= 1

    def resize(self) -> None:
        copy_hash_table = self.hash_table.copy()
        self.hash_table += [None] * self.capacity
        self.capacity *= 2
        for item in copy_hash_table:
            if item:
                del self[item[0]]
                self[item[0]] = item[2]

    def __iter__(self) -> tuple:
        for item in self.hash_table:
            if item:
                yield item

    def clear(self) -> None:
        self.hash_table.clear()
        self.length = 0
