from typing import Any, Hashable

INITIAL_CAPACITY = 8
LOAD_FACTOR = 2 / 3
CAPACITY_MULTIPLIER = 2


class Dictionary:

    def __init__(self,
                 capacity: int = INITIAL_CAPACITY,
                 load_factor: float = LOAD_FACTOR) -> None:
        self.load_factor = load_factor
        self.size = 0
        self.capacity = capacity
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.hash_func(key)
        node = self.hash_table[index]

        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next

        new_node = Node(key, value)
        new_node.next = self.hash_table[index]
        self.hash_table[index] = new_node
        self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.hash_func(key)
        node = self.hash_table[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def hash_func(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        new_hash_table = [None] * self.capacity

        for node in self.hash_table:
            while node:
                index = self.hash_func(node.key)
                new_node = Node(node.key, node.value)
                new_node.next = new_hash_table[index]
                new_hash_table[index] = new_node
                node = node.next

        self.hash_table = new_hash_table


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None
