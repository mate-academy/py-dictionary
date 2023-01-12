import dataclasses
import math
from typing import Any


@dataclasses.dataclass
class Node:
    key: Any
    value: Any


class Dictionary:
    STANDARD_CAPACITY = 8
    THRESHOLD = 2 / 3
    RESIZE = 2

    def __init__(self):
        self.size = 0
        self.capacity = Dictionary.STANDARD_CAPACITY
        self.storage: list = [None] * self.capacity

    def __setitem__(self, key, value):
        index = hash(key) % self.capacity

        if self.size >= math.floor(self.capacity * Dictionary.THRESHOLD):
            self._resize()
            self.__setitem__(key=key, value=value)
            return

        while self.storage[index] is not None:
            if self.storage[index].key == key:
                self.storage[index].value = value
                return

            index = (index + 1) % self.capacity

        self.size += 1
        self.storage[index] = Node(key=key, value=value)

    def _resize(self):
        print("resize")
        self.capacity *= Dictionary.RESIZE
        new_storage = [None] * self.capacity
        old_storage = [i for i in self.storage if i is not None]
        self.size = 0
        self.storage = new_storage

        for node in old_storage:
            self.__setitem__(node.key, node.value)

    def __getitem__(self, item):
        index = hash(item) % self.capacity

        while self.storage[index] is not None:
            if self.storage[index].key == item:
                return self.storage[index].value

            index = (index + 1) % self.capacity

        raise KeyError(f"Key {item} does not exist in Dictionary.")

    def __len__(self):
        return self.size


if __name__ == "__main__":
    test_dict = Dictionary()
