from typing import Hashable


class Dictionary:
    def __init__(
            self,
            capacity: int = 8,
            size: int = 0,
            threshold: float = 0.75
    ) -> None:
        self.capacity = capacity
        self.size = size
        self.threshold = threshold
        self.hash_table = [None] * capacity

    def __setitem__(self, key: Hashable, value: any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, hash_value, value)
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = (key, hash_value, value)
        self.size += 1

        if self.size / self.capacity > self.threshold:
            self.resize()

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_hash_table = [None] * new_capacity

        for item in self.hash_table:
            if item is not None:
                key, hash_value, value = item
                index = hash_value % new_capacity

                while new_hash_table[index] is not None:
                    index = (index + 1) % new_capacity

                new_hash_table[index] = (key, hash_value, value)

        self.capacity = new_capacity
        self.hash_table = new_hash_table

    def __getitem__(self, key: Hashable) -> list:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} is not present in the dictionary.")

    def __len__(self) -> int:
        return self.size
