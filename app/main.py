from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        while True:
            if not self.table[index]:
                self.table[index] = [key, hash(key), value]
                self.size += 1
                break
            if (self.table[index][0] == key
                    and self.table[index][1] == hash(key)):
                self.table[index][2] = value
                break
            index = (index + 1) % self.capacity

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        current = self.table[index]

        while current:
            if current[0] == key and current[1] == hash(key):
                return current[2]
            index = (index + 1) % self.capacity
            current = self.table[index]

        raise KeyError(f"Can't find key: {key}")

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity

        for node in self.table:
            if node:
                index = node[1] % self.capacity
                while new_table[index]:
                    index = (index + 1) % self.capacity
                new_table[index] = node

        self.table = new_table

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.capacity = 8
        self.table = [None] * self.capacity

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        while self.table[index] and self.table[index][0] != key:
            index = (index + 1) % self.capacity

        self.table[index] = None
        self.size -= 1

    def get(self, key: Hashable, value: Any = None) -> Any:
        index = hash(key) % self.capacity
        current = self.table[index]

        while current:
            if current[0] == key and current[1] == hash(key):
                return current[2]
            index = (index + 1) % self.capacity
            current = self.table[index]

        return value

    def pop(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        current = self.table[index]

        while current:
            if current[0] == key and current[1] == hash(key):
                value = current[2]
                self.__delitem__(key)
                return value
            index = (index + 1) % self.capacity
            current = self.table[index]

        raise KeyError(f"Key not found: {key}")

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self.__setitem__(key, value)

    def __iter__(self) -> iter:
        for node in self.table:
            if node:
                yield node[0]
