from typing import Any, Hashable


class Dictionary:

    def __init__(self) -> None:
        self.initial_capacity = 8
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.initial_capacity
        self.size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        if self.size + 1 > self.initial_capacity * self.load_factor:
            self.resize()
        index = hash_value % len(self.hash_table)
        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % len(self.hash_table)
        if self.hash_table[index] is None:
            self.hash_table[index] = [key, hash_value, value]
            self.size += 1
        if self.hash_table[index][0] == key:
            self.hash_table[index][2] = value

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index = hash_value % len(self.hash_table)
        while self.hash_table[index] is not None:
            if (self.hash_table[index][1] == hash_value
                    and self.hash_table[index][0] == key):
                return self.hash_table[index][2]
            index = (index + 1) % len(self.hash_table)
        if self.hash_table[index] is None:
            raise KeyError

    def resize(self) -> None:
        self.initial_capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.initial_capacity
        self.size = 0
        for element in old_hash_table:
            if element:
                self.__setitem__(element[0], element[2])

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.hash_table = [None] * self.initial_capacity

    def __delitem__(self, key: Hashable) -> None:
        try:
            hash_value = hash(key)
            index = hash_value % len(self.hash_table)
            value = self.hash_table[index]
            if value is None:
                raise KeyError

            self.hash_table[index] = [None]
            self.size -= 1
        except TypeError:
            raise
