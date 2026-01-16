from __future__ import annotations

from typing import Any, Dict, Hashable, Iterator, List, Optional, Union


class Node:

    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash_key = hash(key)


class Dictionary:

    LOAD_FACTOR: float = 0.66
    INITIAL_CAPACITY: int = 8

    def __init__(
            self,
            sequence: Optional[Union[Dict, Dictionary]] = None,
            **kwargs: Dict[str, Any]
    ) -> None:
        self.capacity: int = self.INITIAL_CAPACITY
        self.hash_table: List[Optional[Node]] = [None] * self.capacity
        self.size: int = 0
        self.update(sequence, **kwargs)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        node = Node(key, value)
        place = self._place(key)

        while self.hash_table[place]:
            if self.hash_table[place].key == key:
                self.hash_table[place].value = value
                return
            place = (place + 1) % self.capacity

        self.hash_table[place] = node
        self.size += 1
        self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        place = self._place(key)

        while self.hash_table[place]:
            if self.hash_table[place].key == key:
                return self.hash_table[place].value
            place = (place + 1) % self.capacity

        raise KeyError(key)

    def __iter__(self) -> Iterator[Hashable]:
        for node in self.hash_table:
            if node:
                yield node.key

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        hash_key = hash(key)
        place = self._place(hash_key)
        self.hash_table[place] = None
        self.size -= 1

    def __contains__(self, key: Hashable) -> bool:
        hash_key = hash(key)
        place = self._place(hash_key)
        return place in self.hash_table[place]

    def _place(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        if self.size / self.capacity > self.LOAD_FACTOR:
            self.capacity *= 2
            old_hash_table = self.hash_table
            self.hash_table = [None] * self.capacity
            self.size = 0

            for node in old_hash_table:
                if node:
                    self[node.key] = node.value

    def clear(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.hash_table = [None] * self.capacity
        self.size = 0

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        return self[key] if key in self else default

    def pop(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            hash_key = hash(key)
            place = self._place(hash_key)
            value = self.hash_table[place].value
            del self.hash_table[place]
            return value

        except KeyError as error:
            if default:
                return default
            raise error(key)

    def update(
            self,
            other: Optional[Dict, Dictionary],
            **kwargs: Dict[str, Any]
    ) -> None:
        if other and isinstance(other, [Dict, Dictionary]):
            for key in other:
                self[key] = other[key]
        if kwargs:
            for key in kwargs:
                self[key] = kwargs[key]
