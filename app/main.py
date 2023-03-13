from typing import Any


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        table = self.hash_table
        index = self.__index__(key)
        while table[index] is not None and table[index][0] != key:
            index = (index + 1) % self.capacity
        if table[index] is None:
            self.size += 1
        table[index] = (key, hash(key), value)
        if self.size > self.capacity * self.load_factor:
            self.resize()

    def __getitem__(self, item: Any) -> Any:
        index = self.__index__(item)
        try:
            return self.hash_table[index][2]
        except TypeError:
            raise KeyError

    def __len__(self) -> int:
        return self.size

    def __index__(self, key: Any) -> int:
        index = hash(key) % self.capacity
        while (self.hash_table[index] is not None
                and self.hash_table[index][0] != key):
            index = (index + 1) % self.capacity
        return index

    def resize(self) -> None:
        self.capacity *= 2
        old_dict = self.hash_table
        self.hash_table = [None] * self.capacity
        self.size = 0
        for item in old_dict:
            if item is not None:
                self[item[0]] = item[2]

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __delitem__(self, key: Any) -> None:
        index = self.__index__(key)
        if self.hash_table[index] is None:
            raise KeyError
        self.hash_table[index] = None
        self.size -= 1

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            item = self[key]
            del self[key]
            return item
        except KeyError:
            if not default:
                raise KeyError
            return default

    def update(self, other: dict | tuple) -> None:
        iter_other = other if isinstance(other, tuple) else other.items()
        for key, value in iter_other:
            self[key] = value
