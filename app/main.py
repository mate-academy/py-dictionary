from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value
        self.next = None


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.load_factor = 0.75
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.hash_table[index]

        while current is not None:
            if current.hash == hash_value and current.key == key:
                current.value = value
                return

            current = current.next

        new_node = Node(key, value, hash_value)
        new_node.next = self.hash_table[index]
        self.hash_table[index] = new_node
        self.length += 1

        if self.length / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.hash_table[index]

        while current is not None:
            if current.hash == hash_value and current.key == key:
                return current.value

            current = current.next

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_hash_table = self.hash_table

        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_hash_table:
            current = node

            while current is not None:
                self[current.key] = current.value
                current = current.next
