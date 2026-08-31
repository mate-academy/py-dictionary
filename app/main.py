import dataclasses
from typing import Any


@dataclasses.dataclass
class Node:
    key: Any
    hash: int
    value: Any


class Dictionary:

    _threshold_coef = 2 / 3

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._capacity = 8
        self._threshold = round(self._capacity * Dictionary._threshold_coef)
        self._elements = [None] * self._capacity
        self._length = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        index = self._get_index(key, hash_key)

        if self._elements[index] is None:
            self._length += 1
        self._elements[index] = Node(key, hash_key, value)

    def __getitem__(self, key):
        hash_key = hash(key)
        index = self._get_index(key, hash_key)

        if self._elements[index] is None:
            raise KeyError
        return self._elements[index].value

    def __len__(self):
        return self._length

    def _get_index(self, key: Any, hash_key: Any) -> int:
        index = hash_key % self._capacity

        while self._elements[index] is not None and self._elements[index].key != key:
            index += 1
            if index >= self._capacity:
                index %= self._capacity

        return index



d = Dictionary()
d["a"] = 1
d["b"] = 2
d["a"] = 100
print(d._elements)
print(d["a"])