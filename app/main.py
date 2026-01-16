from typing import Any, Hashable


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 2 / 3
                 ) -> None:
        self.initial_capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table = [None] * self.initial_capacity
        self.max_capacity = self.initial_capacity * self.load_factor

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index, hash_of_the_key = self.find_available_index(key)
        if not self.hash_table[index]:
            if self.size >= self.max_capacity:
                self.resize()
            index, hash_of_the_key = self.find_available_index(key)
            self.size += 1
        self.hash_table[index] = [key, hash_of_the_key, value]

    def find_available_index(self, key: Hashable) -> Any:
        hash_of_the_key = hash(key)
        index = hash_of_the_key % self.initial_capacity

        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.initial_capacity
        return index, hash_of_the_key

    def resize(self) -> None:
        self.initial_capacity *= 2
        self.max_capacity = self.initial_capacity * self.load_factor
        self.size = 0

        old_hash_table = self.hash_table.copy()
        self.hash_table = [None] * self.initial_capacity

        for item in old_hash_table:
            if item:
                key, _, value = item
                self[key] = value

    def __getitem__(self, key: Hashable) -> Any:
        index, _ = self.find_available_index(key)
        if self.hash_table[index]:
            return self.hash_table[index][2]
        raise KeyError

    def __len__(self) -> Any:
        return self.size
