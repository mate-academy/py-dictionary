from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self.hash_function(key)

        while (
            self.hash_table[index] is not None
            and self.hash_table[index][0] != key
        ):
            index = (index + 1) % self.capacity

        if self.hash_table[index] is None:
            self.size += 1

        self.hash_table[index] = (key, value)

        if self.size >= self.threshold:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        index = self.hash_function(key)

        for _ in range(self.capacity):
            items = self.hash_table[index]

            if items is None:
                break

            if items[0] == key:
                return items[1]

            index = (index + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def hash_function(self, value: Any) -> int:
        return hash(value) % self.capacity

    def resize(self) -> None:
        self.size = 0
        old_table = self.hash_table[:]
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [None] * self.capacity
        for items in old_table:
            if items is not None:
                self.__setitem__(*items)
