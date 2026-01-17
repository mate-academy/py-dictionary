from typing import Any, Hashable, Iterable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.__capacity = len(self.hash_table)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.__capacity
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.__capacity
        if not self.hash_table[index] or self.hash_table[index][0] == key:
            if not self.hash_table[index]:
                self.length += 1
            self.hash_table[index] = (key, hash(key), value)
        if self.length >= self.__capacity * 2 / 3:
            self.__resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.__capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.__capacity
        raise KeyError(f"Key {key} not in hash table")

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table = [None] * self.__capacity
        self.length = 0

    def __resize(self) -> None:
        old_hash_table = self.hash_table
        self.__capacity *= 2
        self.hash_table = [None] * self.__capacity
        self.length = 0
        for item in old_hash_table:
            if item:
                key, _hash, value = item
                self.__setitem__(key, value)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterable:
        for item in self.hash_table:
            if item:
                for key, _ in item:
                    yield key

    def __delitem__(self, key: Hashable) -> None:
        for index, item in enumerate(self.hash_table):
            if item and item[0] == key:
                self.hash_table[index] = None
                self.length -= 1
                return
        raise KeyError(f"Key {key} not in hash table")

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            pop_value = self[key]
            del self[key]
            return pop_value
        except KeyError:
            return default
