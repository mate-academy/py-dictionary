from typing import Hashable


class Dictionary:
    DEFAULT_CAPACITY = 8
    LOAD_FACTOR = 2 / 3.0

    def __init__(self,
                 capacity: int = DEFAULT_CAPACITY,
                 load_factor: float = LOAD_FACTOR) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.length = 0
        self.hash_table = [None] * capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: any) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, value)
                return
            # handle collision
            index = (index + 1) % self.capacity

        self.hash_table[index] = (key, value)
        self.length += 1

        if self.length / self.capacity >= self.load_factor:
            self.resize()

    def __getitem__(self, key: Hashable) -> any:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            # handling collision
            index = (index + 1) % self.capacity
        raise KeyError(f"key {key} not found")

    def resize(self) -> None:
        # rehash all and double the capacity
        old_htb = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for item in old_htb:
            if item is not None:
                key, value = item
                self[key] = value       # reinsert into new htb
