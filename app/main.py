from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.size: int = 0
        self.load_factor: float = 0.66
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: Hashable, value: Any) -> None:

        index = self.get_index_from_hash(key)

        while True:
            if not self.hash_table[index] or self.hash_table[index][0] == key:
                if not self.hash_table[index]:
                    self.size += 1
                self.hash_table[index] = (key, hash(key), value)

                threshhold = int(self.capacity * self.load_factor)
                if self.capacity - threshhold > self.hash_table.count(None):
                    self.resize()
                break

            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:

        index = self.get_index_from_hash(key)
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(f"key {key} is not found")

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:

        index = self.get_index_from_hash(key)
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = None
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        hash_table = self.hash_table
        self.size = 0
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for item in hash_table:
            if item:
                self.__setitem__(item[0], item[2])

    def get_index_from_hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity
