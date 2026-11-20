from dataclasses import dataclass
from typing import Any


@dataclass()
class Node:
    key: Any
    value: Any
    hash: int  # noqa: VNE003


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.bucket = [None] * self.capacity

    def _find_index(self, key: Any, key_hash: int) -> int:
        index = key_hash % self.capacity
        while self.bucket[index] is not None:
            node = self.bucket[index]
            if node.hash == key_hash and node.key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        old_nodes = [node for node in self.bucket if node is not None]
        self.capacity *= 2
        self.bucket = [None] * self.capacity
        for node in old_nodes:
            index = node.hash % self.capacity
            while self.bucket[index] is not None:
                index = (index + 1) % self.capacity
            self.bucket[index] = node

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_index(key, key_hash)
        if self.bucket[index] is not None:
            self.bucket[index].value = value
            return
        if self.size >= self.capacity * (2 / 3):
            self._resize()
            index = self._find_index(key, key_hash)
        self.bucket[index] = Node(key, value, key_hash)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._find_index(key, key_hash)
        if self.bucket[index] is None:
            raise KeyError(key)
        return self.bucket[index].value

    def __len__(self) -> int:
        return self.size
