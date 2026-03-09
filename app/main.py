from typing import Any, Optional


class Node:
    def __init__(self, key_hash: int, key: Any, value: Any) -> None:
        self.hash = key_hash
        self.key = key
        self.value = value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.length = 0
        self.table: list[Optional[Node]] = [None] * self.capacity
        self.load_factor = 2 / 3

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        self._insert(key_hash, key, value)

        if self.length / self.capacity > self.load_factor:
            self._resize()

    def _insert(self, key_hash: int, key: Any, value: Any) -> None:
        index = key_hash % self.capacity

        while self.table[index] is not None:
            node = self.table[index]
            if node.hash == key_hash and node.key == key:
                node.value = value
                return
            index = (index + 1) % self.capacity

        self.table[index] = Node(key_hash, key, value)
        self.length += 1

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self._insert(node.hash, node.key, node.value)

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] is not None:
            node = self.table[index]
            if node.hash == key_hash and node.key == key:
                return node.value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} not found")
