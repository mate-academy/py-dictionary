from typing import Hashable, Any


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 2 / 3
    ) -> None:
        self.initial_capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table = [None] * initial_capacity

    def hash(self, key: Hashable) -> int:
        index = hash(key) % self.initial_capacity
        while (self.hash_table[index]
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.initial_capacity
        return index

    def resize(self) -> None:
        self.initial_capacity *= 2
        old_table = self.hash_table
        self.hash_table = [None] * self.initial_capacity
        self.size = 0
        for node in old_table:
            if node:
                self.__setitem__(node[0], node[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.load_factor * self.initial_capacity:
            self.resize()
        index = self.hash(key)
        if not self.hash_table[index]:
            self.size += 1
            self.hash_table[index] = [key, hash(key), value]
        if self.hash_table[index][0] == key:
            self.hash_table[index][2] = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self.hash(key)
        if not self.hash_table[index]:
            raise KeyError(key)
        return self.hash_table[index][2]

    def __delitem__(self, key: Hashable) -> None:
        index = self.hash(key)
        if self.hash_table[index] and self.hash_table[index][0] == key:
            self.hash_table[index] = None
            self.size -= 1
        else:
            raise KeyError(key)

    def __iter__(self) -> Hashable:
        for entry in self.hash_table:
            if entry:
                yield entry[0]

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        return str(self.hash_table)
