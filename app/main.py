from __future__ import annotations
from typing import Any, Hashable, Optional, List, Iterable, Tuple
from fractions import Fraction


class Dictionary:
    class _Node:
        def __init__(self, key: Hashable, value: Any) -> None:
            self.key = key
            self.hash_key = hash(key)
            self.value = value

    def __init__(self, load_factor: Fraction = Fraction(2, 3)) -> None:
        self._capacity: int = 8
        self._load_factor: Fraction = load_factor
        self._size: int = 0
        self._buckets: List[Optional[Dictionary._Node]] \
            = [None] * self._capacity

    def _get_index(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def _find_index(self, key: Hashable) -> Tuple[int, bool]:
        index = self._get_index(key)
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                return index, True
            index = (index + 1) % self._capacity
        return index, False

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._size / self._capacity >= self._load_factor:
            self._resize()
        index, found = self._find_index(key)
        if not found:
            self._buckets[index] = self._Node(key, value)
            self._size += 1
        else:
            self._buckets[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index, found = self._find_index(key)
        if not found:
            raise KeyError(f'KeyError: "{key}" not found in Dictionary')
        return self._buckets[index].value

    def __len__(self) -> int:
        return self._size

    def _resize(self) -> None:
        new_capacity = self._capacity * 2
        new_buckets: List[Optional[Dictionary._Node]] = [None] * new_capacity
        for node in self._buckets:
            if node is not None:
                index = node.hash_key % new_capacity
                while new_buckets[index] is not None:
                    index = (index + 1) % new_capacity
                new_buckets[index] = node
        self._buckets = new_buckets
        self._capacity = new_capacity

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._size = 0

    def __delitem__(self, key: Hashable) -> None:
        index, found = self._find_index(key)
        if not found:
            raise KeyError(f'KeyError: "{key}" not found in Dictionary')
        self._buckets[index] = None
        self._size -= 1

        next_index = (index + 1) % self._capacity
        while self._buckets[next_index] is not None:
            node = self._buckets[next_index]
            self._buckets[next_index] = None
            self._size -= 1
            self[node.key] = node.value
            next_index = (next_index + 1) % self._capacity

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is None:
                raise
            return default

    def update(
            self,
            other: dict | Dictionary | Iterable[Tuple[Hashable, Any]]
    ) -> None:
        if other is None:
            return
        if isinstance(other, dict) or isinstance(other, Dictionary):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

    def __iter__(self) -> Iterable[Hashable]:
        for node in self._buckets:
            if node is not None:
                yield node.key
