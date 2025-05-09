from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * 8
        self.threshold = 5

    def hash_index(self, hash_key: int) -> int:
        return hash_key % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        self.length = 0
        old_hash_table = self.hash_table
        self.hash_table: list = [None] * self.capacity
        self.threshold = self.capacity * 2 // 3
        for item in old_hash_table:
            if isinstance(item, tuple):
                self.__setitem__(item[0], item[2])

    def __setitem__(self, key: type | str | int | float | tuple, value: Any) \
            -> None:
        if self.length == self.threshold:
            self.resize()

        hash_key = hash(key)
        index = self.hash_index(hash_key)
        end = index - 1 if index > 0 else self.capacity - 1

        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = (key, hash_key, value)
                self.length += 1
                break
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_key):
                self.hash_table[index] = (key, hash_key, value)
                break
            if index == end:
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: type | str | int | float | tuple) -> Any:
        hash_key = hash(key)
        index = self.hash_index(hash_key)
        end = index - 1 if index > 0 else self.capacity - 1

        while True:
            if (self.hash_table[index] and self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_key):
                return self.hash_table[index][2]
            if index == end:
                raise KeyError(key)
            index = (index + 1) % self.capacity

    def get(
            self, key: type | str | int | float | tuple,
            additional_value: Any = None
    ) -> Any:
        hash_key = hash(key)
        index = self.hash_index(hash_key)
        end = index - 1 if index > 0 else self.capacity - 1

        while True:
            if (self.hash_table[index] and self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_key):
                return self.hash_table[index][2]
            if index == end:
                return additional_value
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table: list = [None] * self.capacity

    def __delitem__(self, key: type | str | int | float | tuple) -> None:
        hash_key = hash(key)
        index = self.hash_index(hash_key)
        end = index - 1 if index > 0 else self.capacity - 1

        while True:
            if (self.hash_table[index] and self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_key):
                self.hash_table[index] = None
                break
            if index == end:
                raise KeyError(key)
            index = (index + 1) % self.capacity

    def pop(self, key: type | str | int | float | tuple) -> Any:
        hash_key = hash(key)
        index = self.hash_index(hash_key)
        end = index - 1 if index > 0 else self.capacity - 1

        while True:
            if (self.hash_table[index] and self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_key):
                returned = self.hash_table[index][2]
                self.hash_table[index] = None
                return returned
            if index == end:
                raise KeyError(key)
            index = (index + 1) % self.capacity

    def update(self, dictionary: "Dictionary") -> None:
        for item in dictionary.hash_table:
            if isinstance(item, tuple):
                self.__setitem__(item[0], item[2])
