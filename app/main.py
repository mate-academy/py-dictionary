from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.length = 0
        self.capacity = capacity
        self.load_factor = load_factor
        self.table = [None] * capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length / self.capacity > self.load_factor:
            self.resize()

        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        old_table = self.table[:]
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0
        for item in old_table:
            if item is not None:
                key, value = item
                self.__setitem__(key, value)

    def clear(self) -> None:
        self.length = 0
        self.capacity = 8
        self.table = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        for _ in range(self.capacity):
            if self.table[index][0] == key:
                self.table[index] = None
                self.length -= 1
                return
            index = (index + 1) % self.capacity

        raise KeyError(key)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError(key):
            return default

    def pop(self, keyname: Hashable, default: Any = None) -> Any:
        try:
            value = self.__getitem__(keyname)
            self.__delitem__(keyname)
            return value
        except KeyError(keyname):
            return default

    def update(self, other: "Dictionary") -> None:
        for key, value in other.table:
            self.__setitem__(key, value)

    def __iter__(self) -> None:
        return (item[0] for item in self.table)
