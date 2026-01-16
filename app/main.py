from typing import Hashable, Any


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.size = 0

    def __get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (
            self.hash_table[index] is not None
            and (
                self.hash_table[index][0] != key
                or self.hash_table[index][2] != hash(key)
            )
        ):
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.__get_index(key)
        if self.hash_table[index] is None:
            self.size += 1
            self.hash_table[index] = [key, value, hash(key)]
        elif self.hash_table[index] is not None:
            self.hash_table[index] = [key, value, hash(key)]
        if self.size >= self.capacity * 2 / 3:
            self.__resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__get_index(key)
        if self.hash_table[index] is None:
            raise KeyError
        return self.hash_table[index][1]

    def __len__(self) -> int:
        return self.size

    def __resize(self) -> None:
        old_hash_table = self.hash_table.copy()
        self.capacity = self.capacity * 2
        self.__clear()
        for cell in old_hash_table:
            if cell is not None:
                self[cell[0]] = cell[1]

    def __clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.size = 0
