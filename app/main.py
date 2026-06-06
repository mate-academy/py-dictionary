from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.initial_capacity: int = 8
        self.current_table_size = self.initial_capacity
        self.load_factor = (2 / 3)
        self.resize_strategy = 2
        self.length = 0
        self.hash_table: list = [None] * self.initial_capacity

    def resize_dict(self) -> None:
        self.current_table_size *= self.resize_strategy
        current_hash_table = self.hash_table
        new_hash_table = [None] * self.current_table_size
        self.hash_table = new_hash_table
        self.length = 0
        for element in current_hash_table:
            if element is not None:
                self[element[0]] = element[1]

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.current_table_size
        if self.hash_table[index] is None:
            self.hash_table[index] = (key, value, hash(key))
            self.length += 1
        elif self.hash_table[index][0] == key:
            self.hash_table[index] = (key, value, hash(key))
        else:
            while self.hash_table[index] is not None:
                index = (index + 1) % self.current_table_size
                if (self.hash_table[index] is not None
                        and self.hash_table[index][0] == key):
                    self.hash_table[index] = (key, value, hash(key))
                    return
            self.hash_table[index] = (key, value, hash(key))
            self.length += 1

        if self.length >= self.current_table_size * self.load_factor:
            self.resize_dict()

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.current_table_size

        if (self.hash_table[index] is not None
                and self.hash_table[index][0] == key):
            return self.hash_table[index][1]

        while self.hash_table[index] is not None:
            index = (index + 1) % self.current_table_size
            if (self.hash_table[index] is not None
                    and self.hash_table[index][0] == key):
                return self.hash_table[index][1]
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.length
