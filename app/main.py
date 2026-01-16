from dataclasses import dataclass
from typing import Hashable, Any, Optional, Iterator


@dataclass
class Node:
    key: Hashable
    value: Any
    key_hash: int


class Dictionary:
    INITIAL_CAPACITY = 8
    THRESHOLD = 0.67
    CAPACITY_MULTIPLIER = 2

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity: int = capacity
        self._size: int = 0
        self._hash_table: list[Optional[Node]] = [None] * self.capacity

    def __len__(self) -> int:
        return self._size

    @property
    def max_size(self) -> int:
        return int(self.capacity * self.THRESHOLD)

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while (node := self._hash_table[index]) is not None:
            if node.key == key and node.key_hash == key_hash:
                break
            index = self._linear_probing(index)
        return index

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        self.capacity *= self.CAPACITY_MULTIPLIER
        self._hash_table = [None] * self.capacity
        self._size = 0

        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)
        if self._hash_table[index] is not None:
            self._hash_table[index].value = value
            return
        if self._size + 1 >= self.max_size:
            self._resize()
            index = self._calculate_index(key)
        self._hash_table[index] = Node(
            key=key, value=value, key_hash=hash(key)
        )
        self._size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        if (node := self._hash_table[index]) is None:
            raise KeyError(f"No such key: {key}")
        return node.value

    def clear(self) -> None:
        self._hash_table = [None] * self.capacity
        self._size = 0

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        index = self._calculate_index(key)
        node = self._hash_table[index]
        return node.value if node is not None else default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterator[Hashable]:
        for node in self._hash_table:
            if node is not None:
                yield node.key
