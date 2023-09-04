from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    key_hash: int
    value: Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self._length = 0
        self._capacity = capacity
        self._load_factor = 2 / 3
        self._capacity_multiplier = 2
        self._hash_table: list[None | Node] = [None] * self._capacity

    def __len__(self) -> int:
        return self._length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self._capacity

        while self._hash_table[index]:
            if self._hash_table[index].key == key:
                self._hash_table[index].value = value
                return

            index = (index + 1) % self._capacity

        if self._length + 1 > self._capacity * self._load_factor:
            self._resize()
            return self.__setitem__(key, value)

        self._hash_table[index] = Node(key, key_hash, value)
        self._length += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self._capacity

        if not self._hash_table[index]:
            raise KeyError

        while self._hash_table[index].key != key:
            index = (index + 1) % self._capacity

        return self._hash_table[index].value

    def _resize(self) -> None:
        previous_nodes = [node for node in self._hash_table if node]
        self.__init__(self._capacity * self._capacity_multiplier)

        for node in previous_nodes:
            self.__setitem__(node.key, node.value)
