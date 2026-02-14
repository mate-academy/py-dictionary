from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        # calculate hash_index
        hash_index = hash(key) % self.capacity
        new_index = self.check_collision(hash_index, key)
        # check if key already in hash_table
        if new_index is not None:
            self.hash_table[new_index][2] = value
        else:
            # calculate new size and call resize if needed
            self.size += 1
            if self.size == round(self.capacity * self.load_factor) + 1:
                self.resize()
                return self.__setitem__(key, value)
            # add new item
            hash_index = self.check_next(hash_index)
            self.hash_table[hash_index] = []
            self.hash_table[hash_index].append(key)
            self.hash_table[hash_index].append(hash(key))
            self.hash_table[hash_index].append(value)

    def __getitem__(self, key: Any) -> object:
        hash_index = hash(key) % self.capacity
        while True:
            if self.hash_table[hash_index] is None:
                raise KeyError(f"Key not found: {key}")
            if (self.hash_table[hash_index][0] == key
                    and self.hash_table[hash_index][1] == hash(key)):
                return self.hash_table[hash_index][2]
            # Collision
            hash_index += 1
            if hash_index >= len(self.hash_table):
                hash_index = 0

    def __len__(self) -> int:
        return self.size

    def check_collision(self, hash_index: int, key: Any) -> None | int:
        while True:
            if self.hash_table[hash_index] is None:
                return None
            if (self.hash_table[hash_index][0] == key
                    and self.hash_table[hash_index][1] == hash(key)):
                return hash_index
            hash_index += 1
            if hash_index >= len(self.hash_table):
                hash_index = 0

    def check_next(self, hash_index: int) -> int:
        while True:
            if self.hash_table[hash_index] is None:
                return hash_index
            hash_index += 1
            if hash_index >= len(self.hash_table):
                hash_index = 0

    def resize(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table.copy()
        self.hash_table = [None] * self.capacity
        self.size = 0
        for element in old_hash_table:
            if element is not None:
                self.__setitem__(element[0], element[2])
