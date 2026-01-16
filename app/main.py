from typing import Any, Optional, List


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash: int = hash_value


class Dictionary:
    def __init__(self, initial_capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.load_factor: float = load_factor
        self.table: List[Optional[Node]] = [None] * self.capacity

    def _find_slot(self, key: Any, hash_value: int) -> int:
        index: int = hash_value % self.capacity
        for _ in range(self.capacity):
            node = self.table[index]
            if node is None or (node.hash == hash_value and node.key == key):
                return index
            index = (index + 1) % self.capacity
        raise RuntimeError("Hashtable is full")

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value: int = hash(key)
        index: int = self._find_slot(key, hash_value)
        if self.table[index] is None:
            self.table[index] = Node(key, value, hash_value)
            self.size += 1
            if self.size / self.capacity > self.load_factor:
                self._resize()
        else:
            # Update value for existing key
            node = self.table[index]
            if node is not None:  # Type guard to satisfy type checker
                node.value = value

    def __getitem__(self, key: Any) -> Any:
        hash_value: int = hash(key)
        index: int = self._find_slot(key, hash_value)
        node = self.table[index]
        if node is None:
            raise KeyError(key)
        return node.value

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table: List[Optional[Node]] = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            if node:
                self.__setitem__(node.key, node.value)
