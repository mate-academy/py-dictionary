import dataclasses
from typing import Any


@dataclasses.dataclass
class Node:
    key: Any
    hash_key: int
    value: Any


class Dictionary:

    _threshold_coef = 2 / 3
    _deleted = object()
    _default = object()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._capacity = 8
        self._threshold = round(self._capacity * Dictionary._threshold_coef)
        self._elements = [None] * self._capacity
        self._length = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        index = self._get_index(key, hash_key)

        if (
                self._elements[index] is None
                or self._elements[index] is self._deleted
        ):
            self._length += 1
        self._elements[index] = Node(key, hash_key, value)

        if self._length >= self._threshold:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = self._get_index(key, hash_key)

        if (
                self._elements[index] is None
                or self._elements[index] is self._deleted
        ):
            raise KeyError
        return self._elements[index].value

    def __delitem__(self, key: Any) -> None:
        hash_key = hash(key)
        index = self._get_index(key, hash_key)

        if (
                self._elements[index] is None
                or self._elements[index] is self._deleted
        ):
            raise KeyError

        self._length -= 1
        self._elements[index] = self._deleted

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Any:
        for element in self._elements:
            if element is None or element is self._deleted:
                continue
            yield element.key

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = _default) -> Any:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default is self._default:
                raise
            return default

    def update(self, other: Dictionary) -> None:
        for element in other._elements:
            if element is None or element is self._deleted:
                continue
            self[element.key] = element.value

    def clear(self) -> None:
        self.__init__()

    def _get_index(self, key: Any, hash_key: Any) -> int:
        index = hash_key % self._capacity

        while (
                self._elements[index] is not None
                and self._elements[index] is not self._deleted
                and self._elements[index].key != key
        ):
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
            if element is None or element is self._deleted:
                continue
            self[element.key] = element.value
