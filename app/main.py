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
        self.size = 0
        self.load_factor = 0.75
        self.table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.table[index]

        while current is not None:
            if current.hash == hash_value and current.key == key:
                current.value = value
                return

            current = current.next

        new_node = Node(key, value, hash_value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1

        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index = hash_value % self.capacity

        current = self.table[index]

        while current is not None:
            if current.hash == hash_value and current.key == key:
                return current.value

            current = current.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table

        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            current = node

            while current is not None:
                self[current.key] = current.value
                current = current.next
