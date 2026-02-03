from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Iterable, Iterator, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")

_DELETED = object()
_MISSING = object()


@dataclass
class _Node(Generic[K, V]):
    key: K
    hash_value: int
    value: V


class Dictionary(Generic[K, V]):
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.66
    ) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")

        capacity = 1
        while capacity < initial_capacity:
            capacity <<= 1

        if not 0.1 <= load_factor <= 0.9:
            raise ValueError("load_factor should be between 0.1 and 0.9")

        self._table: list[_Node[K, V] | object | None]
        self._table = [None] * capacity

        self._size: int = 0
        self._deleted: int = 0
        self._load_factor: float = load_factor

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: K, value: V) -> None:
        if self._needs_resize():
            self._resize(len(self._table) * 2)

        key_hash = hash(key)
        index, found = self._find_slot(key, key_hash, for_insert=True)

        cell = self._table[index]
        if found:
            assert isinstance(cell, _Node)
            cell.value = value
            return

        if cell is _DELETED:
            self._deleted -= 1

        self._table[index] = _Node(key=key, hash_value=key_hash, value=value)
        self._size += 1

    def __getitem__(self, key: K) -> V:
        key_hash = hash(key)
        index, found = self._find_slot(key, key_hash, for_insert=False)
        if not found:
            raise KeyError(key)

        node = self._table[index]
        assert isinstance(node, _Node)
        return node.value

    def __contains__(self, key: K) -> bool:
        key_hash = hash(key)
        _, found = self._find_slot(key, key_hash, for_insert=False)
        return found

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        key_hash = hash(key)
        index, found = self._find_slot(key, key_hash, for_insert=False)
        if not found:
            return default

        node = self._table[index]
        assert isinstance(node, _Node)
        return node.value

    def __delitem__(self, key: K) -> None:
        key_hash = hash(key)
        index, found = self._find_slot(key, key_hash, for_insert=False)
        if not found:
            raise KeyError(key)

        self._table[index] = _DELETED
        self._size -= 1
        self._deleted += 1

        if self._deleted > self._size and len(self._table) > 8:
            self._resize(len(self._table))

    def pop(self, key: K, default: Any = _MISSING) -> V:
        key_hash = hash(key)
        index, found = self._find_slot(key, key_hash, for_insert=False)
        if not found:
            if default is not _MISSING:
                return default  # type: ignore[return-value]
            raise KeyError(key)

        node = self._table[index]
        assert isinstance(node, _Node)
        value = node.value

        self._table[index] = _DELETED
        self._size -= 1
        self._deleted += 1
        return value

    def clear(self) -> None:
        self._table = [None] * len(self._table)
        self._size = 0
        self._deleted = 0

    def update(self, items: Iterable[Tuple[K, V]]) -> None:
        for key, value in items:
            self[key] = value

    def __iter__(self) -> Iterator[K]:
        for cell in self._table:
            if isinstance(cell, _Node):
                yield cell.key

    def items(self) -> Iterator[Tuple[K, V]]:
        for cell in self._table:
            if isinstance(cell, _Node):
                yield (cell.key, cell.value)

    def _needs_resize(self) -> bool:
        used = self._size + self._deleted
        return (used / len(self._table)) >= self._load_factor

    def _resize(self, new_capacity: int) -> None:
        capacity = 1
        while capacity < new_capacity:
            capacity <<= 1

        old_table = self._table
        self._table = [None] * capacity
        self._size = 0
        self._deleted = 0

        for cell in old_table:
            if isinstance(cell, _Node):
                index, _ = self._find_slot(
                    cell.key,
                    cell.hash_value,
                    for_insert=True,
                )
                self._table[index] = _Node(
                    key=cell.key,
                    hash_value=cell.hash_value,
                    value=cell.value,
                )
                self._size += 1

    def _find_slot(
        self,
        key: K,
        key_hash: int,
        *,
        for_insert: bool,
    ) -> Tuple[int, bool]:
        mask = len(self._table) - 1
        index = key_hash & mask

        first_deleted: Optional[int] = None

        while True:
            cell = self._table[index]

            if cell is None:
                if for_insert and first_deleted is not None:
                    return first_deleted, False
                return index, False

            if cell is _DELETED:
                if for_insert and first_deleted is None:
                    first_deleted = index
            else:
                node = cell
                assert isinstance(node, _Node)
                if node.hash_value == key_hash and node.key == key:
                    return index, True

            index = (index + 1) & mask
