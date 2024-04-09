from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * self.capacity

    def _resize_dict(self) -> None:
        old_table = self.hash_table[:]
        self.capacity *= 2
        self.length = 0
        self.hash_table = [None] * self.capacity

        for item in old_table:
            if item is not None:
                self.__setitem__(item[0], item[1])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > len(self.hash_table) * 2 / 3:
            self._resize_dict()

        index = hash(key) % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, value, hash(key)]
                self.length += 1
                return
            if self.hash_table[index][0] and self.hash_table[index][0] == key:
                self.hash_table[index][1] = value
                return
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key} does not exist")

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index]:
                if self.hash_table[index][0] == key:
                    self.hash_table[index] = None
                    self.length -= 1
                index = (index + 1) % self.capacity
            else:
                raise KeyError(f"Key {key} does not exist")

    def get(self, key: Hashable, default: Any = None) -> None:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> None:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other: Any) -> None:
        if isinstance(other, dict):
            other_items = other.items()
        else:
            other_items = other

        for key, value in other_items:
            self.__setitem__(key, value)

    def __iter__(self) -> None:
        for item in self.hash_table:
            if item is not None:
                yield item[0]
