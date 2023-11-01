from typing import Any, Hashable


class Dictionary:

    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.length = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, Hashable):
            raise TypeError(f"'{type(key)}' is unhashable type")
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                self.hash_table[index][2] = value
                return

            index = (index + 1) % self.capacity

        if self.length > self.capacity * self.load_factor:
            self.resize()
            return self.__setitem__(key, value)

        self.hash_table[index] = [key, hash(key), value]
        self.length += 1

    def __getitem__(self, key: int) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.capacity
        if not self.hash_table[index]:
            raise KeyError(f"Key '{key}' is not in dictionary")

        return self.hash_table[index][2]

    def resize(self) -> None:
        self.length = 0
        self.capacity *= 2
        old_table: list[Any] = self.hash_table
        self.hash_table = [None] * self.capacity
        for node in old_table:
            if node:
                self.__setitem__(node[0], node[2])

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return str({node[0]: node[2] for node in self.hash_table if node})

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.capacity
        if not self.hash_table[index]:
            raise KeyError(f"Key '{key}' is not in dictionary")

        self.hash_table.remove(self.hash_table[index])

    def get(self, key: Hashable) -> list[Any]:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.capacity
        if not self.hash_table[index]:
            raise KeyError(f"Key '{key}' is not in dictionary")

        return self.hash_table[index]
