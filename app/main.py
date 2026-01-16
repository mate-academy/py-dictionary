from typing import Any


class Dictionary:

    def __init__(self) -> None:
        self.length = 8
        self.size = 0
        self.hash_table = [None] * self.length

    def find_slot(self, key: Any) -> int:
        index = hash(key) % self.length

        while (
            self.hash_table[index] is not None
            and self.hash_table[index][0] != key
        ):
            index = (index + 1) % self.length
        return index

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.length *= 2
        self.hash_table = [None] * self.length
        self.size = 0

        for element in old_hash_table:
            if element:
                self[element[0]] = element[1]

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.size + 1) / self.length > 0.66:
            self.resize()

        index = self.find_slot(key)
        if self.hash_table[index] is None:
            self.size += 1
        self.hash_table[index] = (key, value)

    def __getitem__(self, key: Any) -> Any:
        index = self.find_slot(key)

        if self.hash_table[index] is None:
            raise KeyError(key)
        return self.hash_table[index][1]

    def __len__(self) -> int:
        return self.size
