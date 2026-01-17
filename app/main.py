from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2 / 3) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        index = hash_key % self.capacity
        if self.table[index] is None:
            self.table[index] = []

        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self.resize()

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for slot in self.table:
            if slot:
                for key, value in slot:
                    new_index = hash(key) % new_capacity
                    if new_table[new_index] is None:
                        new_table[new_index] = []
                    new_table[new_index].append((key, value))

        self.table = new_table
        self.capacity = new_capacity

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        if self.table[index] is None:
            raise KeyError(f"{key} key is not found")

        for k, v in self.table[index]:
            if k == key:
                return v
        raise KeyError(f"{key} key is not found")

    def __len__(self) -> int:
        return self.size
