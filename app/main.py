from typing import Any, Hashable


class Node(object):
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary(object):
    def __len__(self) -> int:
        return self.size

    def __init__(self) -> None:
        self.initial_capacity = 8
        self.table = [None] * self.initial_capacity
        self.load_factor = 2 / 3
        self.size = 0

    def get_hash(self, key: Hashable) -> int:
        return hash(key) % self.initial_capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_hash(key)
        node = Node(key, value)
        while self.table[index] is not None:
            if self.table[index].key == key:
                self.size -= 1
                break
            index = (index + 1) % self.initial_capacity
        self.size += 1
        self.table[index] = node
        if self.size / self.initial_capacity >= self.load_factor:
            self.resize()

    def resize(self) -> None:
        self.initial_capacity *= 2
        self.size = 0
        resized_table = [None] * self.initial_capacity
        table = self.table
        self.table = resized_table
        for node in table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_hash(key)
        if self.table[index] is None:
            raise KeyError
        while self.table[index].key != key:
            index = (index + 1) % self.initial_capacity
            if self.table[index] is None:
                raise KeyError
        return self.table[index].value
