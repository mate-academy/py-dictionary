from typing import Any, Optional, List


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.hash: int = hash(key)
        self.value: Any = value

    def __repr__(self) -> str:
        return f"Node(key={self.key}, hash={self.hash}, value={self.value})"


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.length: int = 0
        self.table: List[Optional[Node]] = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def _index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def _resize(self) -> None:
        old_table: List[Optional[Node]] = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash: int = hash(key)
        index: int = self._index(key_hash)

        while True:
            node = self.table[index]

            if node is None:
                self.table[index] = Node(key, value)
                self.length += 1
                break

            if node.key == key:
                node.value = value
                break

            index = (index + 1) % self.capacity

        if self.length / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash: int = hash(key)
        index: int = self._index(key_hash)

        while True:
            node = self.table[index]

            if node is None:
                raise KeyError(key)

            if node.key == key:
                return node.value

            index = (index + 1) % self.capacity
