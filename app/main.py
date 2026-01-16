from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self) -> None:
        self.length: int = 0
        self.capacity: int = 8
        self.hash_table: list[Node | None] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._get_index(key)
        node = self.hash_table[index]

        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next

        new_node = Node(key, value)
        new_node.next = self.hash_table[index]
        self.hash_table[index] = new_node
        self.length += 1

        if self.length / self.capacity > 0.7:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._get_index(key)
        node = self.hash_table[index]

        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.length

    def _get_index(self, key: Any) -> int:
        hash_value = hash(key) % self.capacity
        return hash_value

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            while node is not None:
                self[node.key] = node.value
                node = node.next

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0
