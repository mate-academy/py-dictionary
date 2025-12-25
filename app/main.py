from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            max_load: float = 2 / 3
    ) -> None:
        self.capacity = initial_capacity
        self.max_load = max_load
        self.length = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        node = Node(key, value)
        if (self.length + 1) > self.capacity * self.max_load:
            self.resize()
        index = self.get_table_index(key)
        if not self.table[index] or self.table[index].key != node.key:
            self.length += 1
        self.table[index] = node

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_table_index(key)
        if self.table[index] is None:
            raise KeyError(key)
        return self.table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_table_index(key)
        self.table[index] = None
        self.length -= 1

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.length = 0
        self.table = [None] * self.capacity
        for node in old_table:
            if node:
                self[node.key] = node.value

    def get_table_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.table[index] and self.table[index].key != key:
            index = (index + 1) % self.capacity
        return index

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.capacity = 8
        self.table = [None] * self.capacity
        self.length = 0
