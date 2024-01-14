from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]
        self.storage = 0

    def __getitem__(self, key: Hashable) -> list:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            try:
                if self.hash_table[index][1] == key and\
                        self.hash_table[index][0] == key_hash:
                    return self.hash_table[index][2]
            except IndexError:
                raise KeyError
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.storage

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if self.storage == self.threshold:
            self.resize()
        key_hash = (hash(key))
        index = key_hash % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key_hash, key, value]
                self.storage += 1
                break
            if self.hash_table[index][1] == key and \
                    self.hash_table[index][0] == key_hash:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            try:
                if self.hash_table[index][1] == key and \
                        self.hash_table[index][0] == key_hash:
                    self.hash_table[index] = []
                    self.storage -= 1
                    return
            except IndexError:
                raise KeyError
            index = (index + 1) % self.capacity

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self.capacity)]
        self.storage = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            try:
                if self.hash_table[index][1] == key and\
                        self.hash_table[index][0] == key_hash:
                    value = self.hash_table[index][2]
                    self.hash_table[index] = []
                    self.storage -= 1
                    return value
            except IndexError:
                if default is not None:
                    return default
                raise KeyError
            index = (index + 1) % self.capacity

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self.__setitem__(key, value)

    def __iter__(self) -> None:
        for item in self.hash_table:
            if item:
                yield item[1]

    def resize(self) -> None:
        hash_table_ = self.hash_table
        self.storage = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in hash_table_:
            if item:
                self.__setitem__(item[1], item[2])
