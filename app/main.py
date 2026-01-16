from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.table_size = 8
        self.hash_table: list = [None] * self.table_size

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        hashed_value = hash(key)
        index = hashed_value % self.table_size
        while self.hash_table[index] is not None:
            saved_key, saved_hashed_value, saved_value = self.hash_table[index]
            if hashed_value == saved_hashed_value and saved_key == key:
                self.hash_table[index] = (key, hashed_value, value)
                break
            index = (index + 1) % len(self.hash_table)
        if self.hash_table[index] is None:
            self.hash_table[index] = (key, hashed_value, value)
            self.length += 1

        if self.length > 2 / 3 * self.table_size:
            self.resize()

    def __getitem__(
            self,
            key: Hashable
    ) -> Any:
        hashed_value = hash(key)
        index = hashed_value % self.table_size
        while True:
            if self.hash_table[index] is None:
                raise KeyError
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.table_size

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        copy_table = [data for data in self.hash_table if data is not None]
        self.table_size *= 2
        self.hash_table = [None] * self.table_size
        self.length = 0
        for key, hashed_value, value in copy_table:
            self.__setitem__(key, value)
