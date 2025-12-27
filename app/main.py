from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> Any:
        index = hash(key) % self.capacity

        if self.table[index] is None:
            self.table[index] = []

        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return

        self.table[index].append([key, value])
        self.size += 1

    def __getitem__(self, item: Any) -> None:
        index = hash(item) % self.capacity

        if self.table[index] is None:
            raise KeyError(f"Key '{item}' not found")

        for pair in self.table[index]:
            if pair[0] == item:
                return pair[1]

        raise KeyError(f"Key '{item}' not found")

    def __len__(self) -> int:
        return self.size
