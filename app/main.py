from typing import Any


class Node:
    def __init__(
            self,
            key: str | int | float | bool | tuple,
            value: Any
    ) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(
            self,
            initial_capacity : int = 8,
            load_factor: float = 0.7
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def _hash(self, key: str | int | float | bool | tuple) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for i in range(self.capacity):
            node = self.table[i]
            while node:
                index = hash(node.key) % new_capacity
                new_node = Node(node.key, node.value)
                new_node.next = new_table[index]
                new_table[index] = new_node
                node = node.next

        self.capacity = new_capacity
        self.table = new_table

    def __setitem__(
            self,
            key: str | int | float | bool | tuple,
            value: Any
    ) -> None:
        index = self._hash(key)
        node = self.table[index]

        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next

        new_node = Node(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: str | int | float | bool | tuple) -> Any:
        index = self._hash(key)
        node = self.table[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size
