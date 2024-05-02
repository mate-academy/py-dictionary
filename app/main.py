from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, coefficient: float = 2 / 3) -> None:
        self.capacity = capacity
        self.hash_table = [None] * capacity
        self.coefficient = coefficient
        self.length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        position = hash(key) % self.capacity
        while self.hash_table[position] is not None:
            if self.hash_table[position][0] == key:
                self.hash_table[position] = (key, value)
                return
            position = (position + 1) % self.capacity

        self.hash_table[position] = (key, value)
        self.length += 1

        if self.length > self.capacity * self.coefficient:
            self._resize_table_capacity()
        del position

    def __getitem__(self, key: Hashable) -> Any:
        position = hash(key) % self.capacity
        while self.hash_table[position] is not None:
            if self.hash_table[position][0] == key:
                return self.hash_table[position][1]
            position = (position + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def _resize_table_capacity(self) -> None:
        self.capacity *= 2
        temp_table = [None] * self.capacity
        for cell in self.hash_table:
            if cell is not None:
                key, value = cell
                index = hash(key) % self.capacity
                while temp_table[index] is not None:
                    index = (index + 1) % self.capacity
                temp_table[index] = (key, value)
        self.hash_table = temp_table
        del temp_table

    def __delitem__(self, key: Hashable) -> None:
        position = hash(key) % self.capacity
        while True:
            if self.hash_table[position] is not None \
                    and self.hash_table[position][0] == key:
                self.hash_table[position] = None
                return
            position = (position + 1) % self.capacity
            if position > self.capacity:
                break
        raise KeyError(key)

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity

    def get(self, key: Hashable) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: Hashable) -> Any:
        temp = self.__getitem__(key)
        self.__delitem__(key)
        return temp
