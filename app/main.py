from typing import Any, Hashable


class Dictionary:
    capacity = 8
    load_factor = 2 / 3
    size = 0

    def __init__(self) -> None:
        self.hash_table = [[None, None]] * (self.capacity + 1)

    def __len__(self) -> int:
        return self.size

    def test_index_paramete(self, index_parameter: int) -> int:
        index_parameter = index_parameter + 1
        if index_parameter > self.capacity:
            index_parameter = 0
        return index_parameter

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.size += 1
        if self.size > self.load_factor * self.capacity:
            self.resize()
        index = hash(key) % self.capacity

        keys = [key[0] for key in self.hash_table]
        if key in keys:
            while keys[index] != key:
                index = self.test_index_paramete(index)
            self.hash_table[index] = [key, value]
            self.size -= 1
        else:
            while self.hash_table[index] != [None, None]:
                index = self.test_index_paramete(index)
            self.hash_table[index] = [key, value]

    def __getitem__(self, find_key: Hashable) -> any:
        coli = 0
        index = hash(find_key) % self.capacity
        while True:
            key_d, val = self.hash_table[index]
            if key_d == find_key:
                return val
            coli += 1
            index = self.test_index_paramete(index)
            if coli > self.capacity * 2:
                raise KeyError("Error due to big count of collisions!!")

    def calculate_index(self, hash_key: int) -> int:
        index = hash_key % self.capacity
        return index

    def resize(self) -> None:
        temp = self.hash_table
        self.capacity *= 2
        self.hash_table = [[None, None]] * (self.capacity + 1)
        for fill_cell in temp:
            if fill_cell != [None, None]:
                key, val = fill_cell
                index = hash(key) % self.capacity
                while self.hash_table[index][0] is not None:
                    index = self.test_index_paramete(index)
                self.hash_table[index] = (key, val)
