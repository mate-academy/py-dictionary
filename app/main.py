from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.load_factor = 2 / 3
        self.hash_table = [None] * capacity

    def __setitem__(self,
                    key: int | str | tuple | float | bytes | bool,
                    value: Any
                    ) -> None:
        if self.__len__() / self.capacity > self.load_factor:
            self.__resize__()

        index = hash(key) % self.capacity

        if self.hash_table[index] is None:
            self.hash_table[index] = (key, value)
        elif self.hash_table[index][0] == key:
            self.hash_table[index] = (key, value)
        else:
            indexx = index
            while (self.hash_table[indexx] is not None
                   and self.hash_table[indexx][0] != key):
                indexx = (indexx + 1) % self.capacity
            self.hash_table[indexx] = (key, value)

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        start_index = index

        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity

            if index == start_index:
                break

        raise KeyError("No key in the dict")

    def __len__(self) -> int:
        length = 0
        for elm in self.hash_table:
            if elm is not None:
                length += 1
        return length

    def __resize__(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity

        for elm in self.hash_table:
            if elm is not None:
                key, value = elm
                index = hash(key) % self.capacity

                while new_table[index] is not None:
                    index = (index + 1) % self.capacity
                new_table[index] = (key, value)

        self.hash_table = new_table
