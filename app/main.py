from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.initial_capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.capacity = 8
        self.table = [None] * 8

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity
        if self.table[index] is None:
            self.table[index] = (key, hash_value, value)
            self.size += 1
            self.check_resize()
        else:
            current = self.table[index]
            while current is not None and current[0] != key:
                index = (index + 1) % self.capacity
                current = self.table[index]
            if current is not None and current[0] == key:
                self.table[index] = (key, hash_value, value)
            else:
                self.table[index] = (key, hash_value, value)
                self.size += 1
                self.check_resize()

    def __getitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        current = self.table[index]

        while current is not None:
            if current[0] == key:
                return current[2]
            index = (index + 1) % self.capacity
            current = self.table[index]

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def check_resize(self) -> None:
        if self.size / self.capacity >= self.load_factor:
            self.resize()

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for entry in self.table:
            if entry is not None:
                key, hash_value, value = entry
                new_index = hash_value % new_capacity
                while new_table[new_index] is not None:
                    new_index = (new_index + 1) % new_capacity
                new_table[new_index] = (key, hash_value, value)
        self.table = new_table
        self.capacity = new_capacity

    def clear(self) -> None:
        self.size = 0
        self.capacity = self.initial_capacity
        self.table = [None] * self.initial_capacity
