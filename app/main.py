from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table_capacity = 8
        self.hash_table: list = [None] * self.hash_table_capacity
        self.hash_table_threshold = self.hash_table_capacity * (2 / 3)

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        position = hash_key % self.hash_table_capacity

        while True:
            if self.hash_table[position] is None:
                self.hash_table[position] = (key, hash_key, value)
                self.length += 1
                break

            if self.hash_table[position][0] == key:
                self.hash_table[position] = (key, hash_key, value)
                break

            position += 1

            if position > self.hash_table_capacity - 1:
                position = 0

        if self.length > self.hash_table_threshold:
            self.rehash()

    def rehash(self) -> None:
        old_hash_table = self.hash_table
        self.hash_table_capacity *= 2
        # self.hash_table_threshold = round(self.hash_table_capacity * (2 / 3))
        self.hash_table_threshold = self.hash_table_capacity * (2 / 3)

        self.hash_table = [None] * self.hash_table_capacity
        self.length = 0

        for item in old_hash_table:
            if item is not None:
                self.__setitem__(item[0], item[2])

    def __getitem__(self, key: Any) -> Any:
        position = hash(key) % self.hash_table_capacity
        count = 0

        while True:
            if self.hash_table[position] is None:
                raise KeyError

            if self.hash_table[position][0] == key:
                return self.hash_table[position][2]

            count += 1
            if count == self.hash_table_capacity:
                raise KeyError

            position += 1

            if position > self.hash_table_capacity - 1:
                position = 0

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.hash_table_capacity = 8
        self.hash_table_threshold = 5

    def __delitem__(self, key: Any) -> None:
        position = hash(key) % self.hash_table_capacity
        count = 0

        while True:
            if self.hash_table[position] is not None \
                    and self.hash_table[position][0] == key:
                self.hash_table[position] = None
                self.length -= 1
                break

            count += 1
            if count == self.hash_table_capacity:
                break

            position += 1

            if position > self.hash_table_threshold - 1:
                position = 0

    def get(self, key: Any, value: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return value

    def pop(self, key: Any) -> None:
        self.__delitem__(key)
