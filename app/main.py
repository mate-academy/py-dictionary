from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if isinstance(key, (list, set, dict)):
            raise TypeError(f"unhashable type of key: {type(key)}")
        if self.length == int(self.capacity * self.load_factor):
            self.resize()
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = (key, hash_key, value)
                self.length += 1
                return
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, hash_key, value)
                return
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        step = 0
        while True:
            step += 1
            if self.hash_table[index] and self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
            if step == self.capacity:
                raise KeyError(f'Key "{key}" does not exist')

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.capacity *= 2
        new_hash_table = [None] * self.capacity
        for items in self.hash_table:
            if items:
                hash_key = hash(items[0])
                index = hash_key % self.capacity
                while True:
                    if new_hash_table[index] is None:
                        new_hash_table[index] = (items[0], hash_key, items[2])
                        break
                    index = (index + 1) % self.capacity
        self.hash_table = new_hash_table
