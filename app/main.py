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

        if self._length >= self._threshold:
            self._resize()

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

    def _resize(self) -> None:
        self._capacity *= 2
        self._threshold = round(self._capacity * Dictionary._threshold_coef)

        elements_copy = self._elements.copy()
        self._elements = [None] * self._capacity
        self._length = 0

        for element in elements_copy:
            if element is None:
                continue
            self[element.key] = element.value



d = Dictionary()
for i in range(20):
    d[f"key{i}"] = i

print(len(d))          # 20
print(d["key5"])       # 5
print(d._capacity)     # 32

try:
    d["nope"]
except KeyError:
    print("KeyError")