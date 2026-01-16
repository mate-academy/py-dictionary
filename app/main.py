from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.threshold = int(self.capacity * (2 / 3))
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.threshold:
            self._resize()

        index = hash(key) % self.capacity
        if self.hash_table[index] is None:
            self.hash_table[index] = [key, value, hash(key)]
            self.length += 1

        else:
            while self.hash_table[index] is not None:
                if self.hash_table[index][0] == key:
                    self.hash_table[index][1] = value
                    return
                index = (index + 1) % self.capacity

            self.hash_table[index] = [key, value, hash(key)]
            self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_table = self.hash_table
        self.length = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * (2 / 3))
        self.hash_table = [None] * self.capacity

        for items in old_table:
            if items is not None:
                self.__setitem__(items[0], items[1])
