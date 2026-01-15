from collections.abc import Hashable
from typing import Any

DEFAULT_CAPACITY = 8
LOAD_FACTOR = 2 / 3


class Dictionary:
    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        self.capacity = capacity
        self.size = 0
        self.box = [None] * self.capacity

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_box = [None] * new_capacity
        for item in self.box:
            if item is not None:
                key, value = item
                index = hash(key) % new_capacity
                while new_box[index] is not None:
                    index = (index + 1) % new_capacity
                new_box[index] = (key, value)
        self.box = new_box
        self.capacity = new_capacity

    def index_key(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.box[index] is not None:
            _key, _value = self.box[index]
            if _key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.index_key(key)
        if self.box[index] is None:
            self.size += 1
        self.box[index] = (key, value)
        if self.size >= self.capacity * LOAD_FACTOR:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.index_key(key)
        if self.box[index] is None:
            raise KeyError
        return self.box[index][1]

    def __len__(self) -> int:
        return self.size
