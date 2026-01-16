from typing import Any, Hashable


class Dictionary:
    class Node:
        def __init__(self, key: Hashable, value: Any) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)

    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self._resize()

        index = self._hash(key)
        node = self.hash_table[index]

        while node:
            if node.key == key:
                node.value = value
                return
            index = (index + 1) % self.capacity
            node = self.hash_table[index]

        self.hash_table[index] = self.Node(key, value)
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._hash(key)
        node = self.hash_table[index]

        while node:
            if node.key == key:
                return node.value
            index = (index + 1) % self.capacity
            node = self.hash_table[index]

        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_hash_table = [node for node in self.hash_table if node]
        self.capacity *= 2
        self.size = 0
        self.hash_table = [None] * self.capacity

        for node in old_hash_table:
            self.__setitem__(node.key, node.value)
