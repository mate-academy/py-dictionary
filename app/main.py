from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.table: Any = [None] * self.capacity
        self.load_factor = 0.75
        self.threshold = self.capacity * self.load_factor
        self.items = 0

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.threshold = self.capacity * self.load_factor

        for item in old_table:
            if item is not None:
                key, hash_key, value = item
                index = hash_key % self.capacity
                while self.table[index] is not None:
                    index = (index + 1) % self.capacity
                self.table[index] = (key, hash_key, value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while self.table[index] is not None:
            k, h, v = self.table[index]
            if k == key:
                self.table[index] = (key, hash_key, value)
                return
            index = (index + 1) % self.capacity

        if self.items + 1 > self.threshold:
            self._resize()
            index = hash_key % self.capacity
            while self.table[index] is not None:
                index = (index + 1) % self.capacity

        self.items += 1
        self.table[index] = (key, hash_key, value)

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity

        while self.table[index] is not None:
            k, h, v = self.table[index]
            if k == key:
                return v
            index = (index + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self.items
