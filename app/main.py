from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Node:
    hash: int
    key: int
    value: Any


class Dictionary:
    _DEFAULT_LENGTH = 8
    _LOAD_FACTOR = 2 / 3
    _RESIZE = 2

    def __init__(self):
        self._hashtable: List[Optional[Node]] = \
            [None for _ in range(Dictionary._DEFAULT_LENGTH)]
        self._size = 0
        self._capacity = Dictionary._DEFAULT_LENGTH

    def __len__(self):
        return self._size

    def __getitem__(self, item):
        hash_ = hash(item)
        index = hash_ % self._capacity
        while self._hashtable[index] is not None:
            if self._hashtable[index].key == item:
                return self._hashtable[index].value
            index = (index + 1) % self._capacity
        raise KeyError

    def _resize(self):
        previous_nodes = [node for node in self._hashtable if node is not None]
        self._capacity *= Dictionary._RESIZE
        self._hashtable = [None for _ in range(self._capacity)]
        self._size = 0

        for node in previous_nodes:
            self.__setitem__(node.key, node.value)

    def __setitem__(self, key, value):
        hash_ = hash(key)
        index = hash_ % self._capacity

        while self._hashtable[index] is not None:
            current_node = self._hashtable[index]

            if hash_ == current_node.hash and key == current_node.key:
                current_node.value = value
                return
            index = (index + 1) % self._capacity

        self._hashtable[index] = Node(hash_, key, value)
        self._size += 1

        if (self._size + 1) > Dictionary._LOAD_FACTOR * self._capacity:
            self._resize()
