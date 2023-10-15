from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.table = [[None] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= int(self.capacity * self.load_factor):
            self.resize()
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            if self.table[index][0] == key or (self.table[index] == [None]):
                if self.table[index] == [None]:
                    self.size += 1
                self.table[index] = [key, value]
                break
            else:
                index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any | KeyError:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while self.table[index] != [None]:
            if key == self.table[index][0]:
                return self.table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError("Key not found")

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[None] for _ in range(self.capacity)]
        for key_value in old_table:
            if key_value != [None]:
                key_hash = hash(key_value[0])
                index = key_hash % self.capacity
                while True:
                    if key_value[0] == self.table[index][0] or \
                            (self.table[index] == [None]):
                        self.table[index] = [key_value[0], key_value[1]]
                        break
                    index = (index + 1) % self.capacity

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        for _ in range(self.capacity):
            if key == self.table[index][0]:
                self.table[index] = [None]
                self.size -= 1
                break
            index = (index + 1) % self.capacity

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default_value

    def pop(self, key: Hashable, default_value: Any = None) -> Any:
        if default_value is None:
            default_value = self.get(key, default_value)
        self.__delitem__(key)
        return default_value

    def update(self, other: Dictionary) -> None:
        for elem in other.table:
            if elem == [None]:
                continue
            self.__setitem__(elem[0], elem[1])
