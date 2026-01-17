from typing import Any


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.666
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    class Node:
        def __init__(self, key: Any, value: Any) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)
            self.next = None

    def __setitem__(self, key: Any, value: Any) -> None:
        node_hash = hash(key)
        index = node_hash % self.capacity

        if self.table[index] is None:
            self.table[index] = self.Node(key, value)
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    current.next = self.Node(key, value)
                    break
                current = current.next

        self.size += 1
        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> None:
        node_hash = hash(key)
        index = node_hash % self.capacity

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for bucket in old_table:
            current = bucket
            while current:
                self[current.key] = current.value
                current = current.next
