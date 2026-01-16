from typing import Any, Optional


class Dictionary:
    initial_capacity: int = 8
    load_factor: float = 2 / 3

    class Node:
        def __init__(self, key: Any, hash_value: int, value: Any) -> None:
            self.key = key
            self.hash_value = hash_value
            self.value = value
            self.next: Optional["Dictionary.Node"] = None

    def __init__(self) -> None:
        self.capacity = self.initial_capacity
        self.size = 0
        self.table: list[Optional[Dictionary.Node]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self._resize()

        hash_value: int = hash(key)
        index: int = self._index(hash_value)

        if not self.table[index]:
            self.table[index] = self.Node(key, hash_value, value)
        else:
            node: Optional[Dictionary.Node] = self.table[index]
            while node:
                if node.hash_value == hash_value and node.key == key:
                    node.value = value
                    return
                if not node.next:
                    break
                node = node.next
            node.next = self.Node(key, hash_value, value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value: int = hash(key)
        index = self._index(hash_value)
        node: Optional[Dictionary.Node] = self.table[index]

        while node:
            if node.hash_value == hash_value and node.key == key:
                return node.value
            node = node.next
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table: list[Optional[Dictionary.Node]] = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            while node:
                self[node.key] = node.value
                node = node.next

    def _index(self, hash_value: int) -> int:
        return hash_value % self.capacity
