import dataclasses
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.size: int = 0
        self.capacity: int = 8
        self.node = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: Hashable, value: Any) -> Any:
        index = hash(key) % self.capacity
        treshold = self.capacity * 2 / 3
        while self.node[index] is not None:
            if self.node[index].key == key:
                self.node[index].value = value
                return
            index = (index + 1) % self.capacity
        if self.size > treshold:
            self.resize_hashtable()
            self.__setitem__(key=key, value=value)
            return
        self.size += 1
        self.node[index] = Node(key=key, value=value, hash_=hash(key))

    def resize_hashtable(self) -> None:
        self.capacity *= 2
        items = [item for item in self.node if item is not None]
        self.size = 0
        self.node = [None] * self.capacity
        for item in items:
            self.__setitem__(item.key, item.value)

    def __getitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        while self.node[index] is not None:
            if self.node[index].key == key:
                return self.node[index].value
            index = (index + 1) % self.capacity
        raise KeyError("Dictionary key is not found")


@dataclasses.dataclass
class Node:
    key: Any
    value: Any
    hash_: Any
