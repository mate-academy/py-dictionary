from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.load_factor = 2 / 3
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        while True:
            if self.keys[index] is None:
                self.keys[index] = key
                self.values[index] = value
                self.length += 1
                break
            if self.keys[index] == key:
                self.values[index] = value
                break
            index = (index + 1) % self.capacity
        if self.length > self.capacity * self.load_factor:
            self.resize()

    def resize(self) -> None:
        old_keys = self.keys
        old_values = self.values
        self.capacity *= 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.length = 0
        for i in range(len(old_keys)):
            if old_keys[i] is not None:
                self[old_keys[i]] = old_values[i]

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while True:
            if self.keys[index] == key:
                return self.values[index]
            if self.keys[index] is None:
                raise KeyError(f"Key {key!r} not found")
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.length = 0
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
