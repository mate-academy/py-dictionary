from typing import Any, Hashable, List, Optional
from fractions import Fraction


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor = Fraction(2, 3)
        self.table: List[Optional[List[Node]]] = [None] * self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for bucket in old_table:
            if bucket:
                for node in bucket:
                    self.__setitem__(node.key, node.value)

    def _hash_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _find_node(
        self,
        bucket: Optional[List[Node]],
        key: Hashable
    ) -> Optional[Node]:
        if bucket:
            for node in bucket:
                if node.key == key:
                    return node
        return None

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()

        index = self._hash_index(key)
        if self.table[index] is None:
            self.table[index] = []

        node = self._find_node(self.table[index], key)
        if node:
            node.value = value
        else:
            self.table[index].append(Node(key, value))
            self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._hash_index(key)
        bucket = self.table[index]
        node = self._find_node(bucket, key)
        if node:
            return node.value
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size
