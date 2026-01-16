from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.data = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> Any:
        index = hash(key) % self.capacity
        if self.data[index] is None:
            self.data[index] = []

        for pairs in self.data[index]:
            if pairs[0] == key:
                pairs[1] = value
                return
        self.data[index].append([key, value])
        self.size += 1

    def __getitem__(self, item: Any) -> Any:
        index = hash(item) % self.capacity
        if self.data[index] is None:
            raise KeyError

        for pairs in self.data[index]:
            if pairs[0] == item:
                return pairs[1]

    def __len__(self) -> int:
        return self.size
