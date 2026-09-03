from dataclasses import dataclass
from typing import Any, Hashable


@dataclass(slots=True)
class Node:
    key: Hashable
    value: Any
    _hash: int


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 0.75
    RESIZE_MULTIPLIER = 2

    def __init__(self) -> None:
        self._size = 0
        self._hash_table = [None] * self.INITIAL_CAPACITY
        self._capacity = self.INITIAL_CAPACITY

    @property
    def _max_size(self) -> int | float:
        return self._capacity * self.LOAD_FACTOR

    def resize(self) -> None:
        if self._size >= self._max_size:
            self._capacity *= 2
            old_table = self._hash_table
            self._hash_table = [None] * self._capacity
            for node in old_table:
                if node is not None:
                    index = node._hash % self._capacity
                    while self._hash_table[index] is not None:
                        index = (index + 1) % self._capacity
                    self._hash_table[index] = node

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.resize()
        key_hash = hash(key)
        index = key_hash % self._capacity
        while self._hash_table[index] is not None:
            if self._hash_table[index].key == key:
                self._hash_table[index].value = value
                return
            index = (index + 1) % self._capacity
        self._hash_table[index] = Node(key, value, key_hash)
        self._size += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self._capacity
        while self._hash_table[index] is not None:
            if self._hash_table[index].key == key:
                return self._hash_table[index].value
            index = (index + 1) % self._capacity
        raise KeyError("Key not found")


if __name__ == "__main__":
    dict_ = Dictionary()
