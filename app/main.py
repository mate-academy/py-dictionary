from typing import Any


class Dictionary:
    class Node:
        def __init__(self, key: str, value: Any) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)

    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor_threshold = 0.75
        self.table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: str, value: Any) -> None:
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

        index = self._get_index(key)
        for node in self.table[index]:
            if node.key == key:
                node.value = value
                return

        self.table[index].append(self.Node(key, value))
        self.size += 1

    def __getitem__(self, key: str) -> Any:
        index = self._get_index(key)

        for node in self.table[index]:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size

    def _get_index(self, key: str) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]

        for bucket in self.table:
            for node in bucket:
                index = node.hash % new_capacity
                new_table[index].append(node)

        self.table = new_table
        self.capacity = new_capacity
