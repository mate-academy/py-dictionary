from typing import Any, Hashable


class Dictionary:

    def __init__(self) -> None:
        self.length = 0
        self.hash_table = [None] * 8
        self.length_hash_table = 8

    @staticmethod
    def index_table(key: Hashable, table: int) -> int:
        if table != 0:
            return hash(key) % table

    def _resize(self) -> None:
        self.length_hash_table *= 2
        index = 0
        old_hash = self.hash_table
        self.hash_table = [None] * self.length_hash_table

        for data in old_hash:
            if data is not None:
                key, value = data[0], data[1]
                index = self.index_table(key, self.length_hash_table)

                while True:
                    if self.hash_table[index] is None:
                        break
                    if index == self.length_hash_table - 1:
                        index = 0
                        continue
                    index += 1

                self.hash_table[index] = [key, value, hash(key)]

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if self.length > self.length_hash_table * 2 / 3:
            self._resize()

        index = self.index_table(key, self.length_hash_table)

        while True:
            if ((self.hash_table[index] is None)
                    or (self.hash_table[index][0] == key)):
                break
            if index == self.length_hash_table - 1:
                index = 0
                continue
            index += 1

        if self.hash_table[index] is None:
            self.length += 1

        self.hash_table[index] = [key, value, hash(key)]

    def __getitem__(self, key: Hashable) -> Any:
        index = self.index_table(key, self.length_hash_table)

        if self.hash_table[index] is None:
            raise KeyError

        while True:
            if self.hash_table[index][0] == key:
                break
            if index == self.length_hash_table - 1:
                index = 0
                continue
            index += 1
        return self.hash_table[index][1]

    def __len__(self) -> int:
        return self.length
