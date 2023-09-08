import dataclasses
import math
from typing import Any


@dataclasses.dataclass
class Node:
    key: Any
    value: Any


class Dictionary:
    def __init__(self):
        self.size = 0
        self.capacity = 8
        self.data = [None] * self.capacity

    def __setitem__(self, key, value):

        index = hash(key) % self.capacity

        while self.data[index] is not None:
            if self.data[index].key == key:
                self.data[index].value = value
                return

            index = (index + 1) % self.capacity

        if self.size >= math.floor(self.capacity * 2 // 3):
            self._resize_data()
            self.__setitem__(key=key, value=value)
            return

        self.size += 1
        self.data[index] = Node(key=key, value=value)

    def __getitem__(self, key):
        index = hash(key) % self.capacity
        while self.data[index] is not None:
            if self.data[index].key == key:
                return self.data[index].value
            index = (index + 1) % self.capacity
        raise KeyError("Key not found")

    def _resize_data(self):
        self.capacity *= 2
        items = [item for item in self.data if item is not None]
        self.size = 0
        self.data = [None] * self.capacity
        for item in items:
            self.__setitem__(item.key, item.value)

    def __len__(self):
        return self.size
