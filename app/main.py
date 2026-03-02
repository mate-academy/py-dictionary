from dataclasses import dataclass

from typing import Any, List, Optional


@dataclass
class Node:
    hash: int
    key: Any
    value: Any


class Dictionary:
    _DEFAULT_LENGTH = 8
    _LOAD_COEFFICIENT = 2 / 3
    _RESIZE = 2

    def __init__(self):
        self._hash_table: List[Optional[Node]] = [
            None for _ in range(Dictionary._DEFAULT_LENGTH)
        ]
        self._size = 0
        self._capacity = Dictionary._DEFAULT_LENGTH

    def __getitem__(self, key):
        hash_ = hash(key)
        index = hash_ % self._capacity
        while self._hash_table[index] is not None:
            if hash_ == self._hash_table[index].hash \
                    and key == self._hash_table[index].key:
                return self._hash_table[index].value
            index = (index + 1) % self._capacity
        raise KeyError(key)

    def __setitem__(self, key, value):
        hash_ = hash(key)
        index = hash_ % self._capacity

        while self._hash_table[index] is not None:
            current_node = self._hash_table[index]
            if hash_ == current_node.hash and key == current_node.key:
                current_node.value = value
                return
            index = (index + 1) % self._capacity
        self._hash_table[index] = Node(hash_, key, value)
        self._size += 1
        if (self._size + 1) > Dictionary._LOAD_COEFFICIENT * self._capacity:
            self._resize()

    def _resize(self):
        existing_nodes = [
            node for node in self._hash_table if node is not None
        ]
        self._capacity *= Dictionary._RESIZE
        self._hash_table = [None for _ in range(self._capacity)]
        self._size = 0
        for node in existing_nodes:
            self[node.key] = node.value

    def __len__(self):
        return self._size
