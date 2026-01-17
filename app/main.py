from typing import Any, Optional, List


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.hash: int = hash(key)
        self.value: Any = value


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 2 / 3
                 ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.table: List[Optional[Node]] = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def _find_slot(self, key_hash: int, key: Any) -> int:
        index: int = key_hash % self.capacity
        while self.table[index] is not None:
            if self.table[index].key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        old_table: List[Optional[Node]] = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [None] * self.capacity
        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size + 1 > int(self.capacity * self.load_factor):
            self._resize()

        key_hash = hash(key)
        index = self._find_slot(key_hash, key)

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            self.table[index].value = value

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        initial_index = index

        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity
            if index == initial_index:
                break

        raise KeyError(f"Key {key} not found.")
