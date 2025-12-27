from typing import Any, Hashable, Iterator, Iterable, Tuple
from collections import namedtuple


Node = namedtuple("Node", ["key", "value", "hash_value"])


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.67) -> None:
        self._capacity = capacity
        self._load_factor = load_factor
        self.length = 0
        self.hash_table = [None] * self._capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self._capacity
        for range_index in range(self._capacity):
            next_index = (index + range_index) % self._capacity
            node = self.hash_table[next_index]
            if node is None:
                self.hash_table[next_index] = Node(key, value, hash_value)
                self.length += 1
                if self.length > self._capacity * self._load_factor:
                    self._resize()
                break
            elif node.key == key:
                new_node = Node(key, value, hash_value)
                self.hash_table[next_index] = new_node
                break

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index = hash_value % self._capacity
        for range_index in range(self._capacity):
            next_index = (index + range_index) % self._capacity
            node = self.hash_table[next_index]
            if node is None:
                break
            if node.key == key:
                return node.value
        raise KeyError(f"Key '{key}' not found")

    def __iter__(self) -> Iterator:
        for node in self.hash_table:
            if node is not None:
                yield node.key

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = hash_value % self._capacity
        for range_index in range(self._capacity):
            next_index = (index + range_index) % self._capacity
            node = self.hash_table[next_index]
            if node is None:
                raise KeyError(f"Key '{key}' not found")
            if node.key == key:
                self.hash_table[next_index] = None
                self.length -= 1
                self._resize(new_capacity=self._capacity)
                return

    def _resize(self, new_capacity: int = None) -> None:
        if new_capacity is None:
            new_capacity = self._capacity * 2
        old_table = self.hash_table
        self.hash_table = [None] * new_capacity
        self.length = 0
        self._capacity = new_capacity
        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def clear(self) -> None:
        self.hash_table = [None] * self._capacity
        self.length = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default

    def update(self, other: Iterable[Tuple]) -> None:
        if isinstance(other, Dictionary):
            for key in other:
                self[key] = other[key]
        elif isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            for item in other:
                if isinstance(item, tuple) and len(item) == 2:
                    key, value = item
                    self[key] = value
                else:
                    raise TypeError("Iterable with tuples expected")
