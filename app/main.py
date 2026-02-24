from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.length = 0
        self.load_factor = 0.625
        self.table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        node = Node(key, value)
        index = node.hash % self.capacity
        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index].value = value
                return
            else:
                index = (index + 1) % self.capacity
        self.table[index] = node
        self.length += 1
        if self.length / self.capacity >= self.load_factor:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            else:
                index = (index + 1) % self.capacity
        raise KeyError(key)

    def resize(self) -> None:
        temp = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0
        for i in temp:
            if i is not None:
                self.__setitem__(i.key, i.value)

    def clear(self) -> None:
        self.length = 0
        self.table = [None] * self.capacity
