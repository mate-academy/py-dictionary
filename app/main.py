from typing import Any, Iterable
from dataclasses import dataclass
from collections import defaultdict

INITIAL_CAPACITY = 8
LOAD_FACTOR = 2 / 3


@dataclass
class Dictionary:
    @dataclass
    class Node:
        key: Any
        value: Any
        hash_value: int

    def __init__(
            self,
            initial_capacity: int = INITIAL_CAPACITY,
            load_factor: float = LOAD_FACTOR
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = defaultdict(list)

    def _calculate_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _find_node(self, key: Any, index: int) -> Node | None:
        hash_value = hash(key)
        for node in self.table[index]:
            if node.hash_value == hash_value and node.key == key:
                return node
        return None

    def _resize(self) -> None:
        if self.size / self.capacity >= self.load_factor:
            self.capacity *= 2
            new_table = defaultdict(list)

            for bucket in self.table.values():
                for node in bucket:
                    index = node.hash_value % self.capacity
                    new_table[index].append(node)

            self.table = new_table

            for bucket in new_table.values():
                for node in bucket:
                    self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._calculate_index(key)
        node = self._find_node(key, index)
        if node:
            node.value = value
        else:
            self.table[index].append(self.Node(key, value, hash(key)))
            self.size += 1
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._calculate_index(key)
        node = self._find_node(key, index)
        if node:
            return node.value
        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        index = self._calculate_index(key)
        node = self._find_node(key, index)
        if node:
            self.table[index].remove(node)
            self.size -= 1
        else:
            raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> None:
        for bucket in self.table.values():
            for node in bucket:
                yield node.key, node.value

    def update(self, other: dict | Iterable[tuple[Any, Any]]) -> None:
        if isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self.table.clear()
        self.size = 0

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise KeyError(key)
