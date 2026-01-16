from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table: list = [[]] * self.capacity
        self.size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        node = [key, hash(key), value]
        if self.size / self.capacity > self.load_factor:
            self.resize()
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = node
                self.size += 1
                break
            if (
                self.hash_table[index][0] == node[0]
                and self.hash_table[index][1] == node[1]
            ):
                self.hash_table[index][2] = node[2]
                break
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        self.size = 0
        hash_table = self.hash_table
        self.hash_table: list = [[]] * self.capacity
        for node in hash_table:
            if node:
                self.__setitem__(node[0], node[2])

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            if (
                self.hash_table[index][1] == hash(key)
                and self.hash_table[index][0] == key
            ):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(f"Cannot find value with key: {key}")

    def __len__(self) -> int:
        return self.size
