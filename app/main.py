from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Generic,
)

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _Node(Generic[K, V]):
    key: K
    hash_value: int
    value: V


_EMPTY = object()
_DELETED = object()


class Dictionary(Generic[K, V]):

    def __init__(
        self,
        initial_capacity: int = 8,
        load_factor: float = 2.0 / 3.0,
    ) -> None:
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")

        capacity = 1
        while capacity < initial_capacity:
            capacity <<= 1

        self._table: List[object] = [_EMPTY] * capacity
        self._size: int = 0
        self._tombstones: int = 0
        self._load_factor: float = load_factor
        self._threshold: int = int(capacity * load_factor)

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: K, value: V) -> None:
        if (self._size + self._tombstones + 1) > self._threshold:
            self._resize(len(self._table) * 2)
        self._insert_or_update(key, value)

    def __getitem__(self, key: K) -> V:
        index, found = self._find_slot(key)
        if not found:
            raise KeyError(key)
        node = self._table[index]
        assert isinstance(node, _Node)
        return node.value

    def __contains__(self, key: K) -> bool:
        _, found = self._find_slot(key)
        return found

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        index, found = self._find_slot(key)
        if not found:
            return default
        node = self._table[index]
        assert isinstance(node, _Node)
        return node.value

    def clear(self) -> None:
        self._table = [_EMPTY] * max(8, len(self._table))
        self._size = 0
        self._tombstones = 0
        self._threshold = int(len(self._table) * self._load_factor)

    def __delitem__(self, key: K) -> None:
        index, found = self._find_slot(key)
        if not found:
            raise KeyError(key)
        self._table[index] = _DELETED
        self._size -= 1
        self._tombstones += 1

    def pop(self, key: K, default: object = _EMPTY) -> V:
        index, found = self._find_slot(key)
        if not found:
            if default is _EMPTY:
                raise KeyError(key)
            return default
        node = self._table[index]
        assert isinstance(node, _Node)
        self._table[index] = _DELETED
        self._size -= 1
        self._tombstones += 1
        return node.value

    def update(
        self,
        pairs: Iterable[Tuple[K, V]] | "Dictionary[K, V]" | object,
    ) -> None:
        it: Iterable[Tuple[K, V]]
        if hasattr(pairs, "items"):
            it = getattr(pairs, "items")()
        else:
            it = pairs
        for key, value in it:
            self[key] = value

    def __iter__(self) -> Iterator[K]:
        for slot in self._table:
            if isinstance(slot, _Node):
                yield slot.key

    def items(self) -> Iterator[Tuple[K, V]]:
        for slot in self._table:
            if isinstance(slot, _Node):
                yield (slot.key, slot.value)

    def values(self) -> Iterator[V]:
        for slot in self._table:
            if isinstance(slot, _Node):
                yield slot.value

    def keys(self) -> Iterator[K]:
        return iter(self)

    def __repr__(self) -> str:
        parts = []
        for k, v in self.items():
            parts.append(f"{repr(k)}: {repr(v)}")
        joined = ", ".join(parts)
        return f"Dictionary({{{joined}}})"

    def _resize(self, new_capacity: int) -> None:
        capacity = 1
        while capacity < new_capacity:
            capacity <<= 1

        old_table = self._table
        self._table = [_EMPTY] * capacity
        self._size = 0
        self._tombstones = 0
        self._threshold = int(capacity * self._load_factor)

        for slot in old_table:
            if isinstance(slot, _Node):
                self._insert_no_resize(
                    slot.key,
                    slot.value,
                    slot.hash_value,
                )

    def _insert_no_resize(
        self,
        key: K,
        value: V,
        hash_value: int,
    ) -> None:
        mask = len(self._table) - 1
        index = hash_value & mask

        first_deleted_index: Optional[int] = None
        while True:
            slot = self._table[index]
            if slot is _EMPTY:
                target = (
                    first_deleted_index
                    if first_deleted_index is not None
                    else index
                )
                self._table[target] = _Node(key, hash_value, value)
                self._size += 1
                if first_deleted_index is not None:
                    self._tombstones -= 1
                return
            if slot is _DELETED:
                if first_deleted_index is None:
                    first_deleted_index = index
            else:
                assert isinstance(slot, _Node)
                same_hash = slot.hash_value == hash_value
                if same_hash and slot.key == key:
                    slot.value = value
                    return
            index = (index + 1) & mask

    def _insert_or_update(self, key: K, value: V) -> None:
        hash_value = hash(key)
        self._insert_no_resize(key, value, hash_value)

    def _find_slot(self, key: K) -> Tuple[int, bool]:
        hash_value = hash(key)
        mask = len(self._table) - 1
        index = hash_value & mask

        while True:
            slot = self._table[index]
            if slot is _EMPTY:
                return index, False
            if slot is _DELETED:
                index = (index + 1) & mask
                continue
            assert isinstance(slot, _Node)
            same_hash = slot.hash_value == hash_value
            if same_hash and slot.key == key:
                return index, True
            index = (index + 1) & mask
