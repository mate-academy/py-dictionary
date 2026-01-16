from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.threshold = int(self.capacity * self.load_factor)
        self.length = 0
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * self.load_factor)
        self.length = 0
        old_table = self.hash_table
        self.hash_table = [None] * self.capacity
        for item in old_table:
            if item:
                self.__setitem__(item[0], item[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        key_hash_value = [key, key_hash, value]
        index = key_hash % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = key_hash_value
                self.length += 1
                break
            if self.hash_table[index][:2] == key_hash_value[:2]:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

        if self.length > self.threshold:
            self.resize()

    def __getitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.capacity
        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")
        return self.hash_table[index][2]

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        if self.hash_table[index] is None:
            raise KeyError(key)
        self.hash_table[index] = None
        self.length -= 1
