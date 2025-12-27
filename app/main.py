from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(
            self,
            capacity: int = 8,
            resize_threshold: float = 2 / 3,
            capacity_multiplier: int = 2
    ) -> None:

        self.capacity = capacity
        self.resize_threshold = resize_threshold
        self.capacity_multiplier = capacity_multiplier
        self.hash_table: list[Node | None] = [None] * self.capacity
        self.length = 0

    @property
    def current_max_size(self) -> float:
        return self.resize_threshold * self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while self.hash_table[index] and self.hash_table[index].key != key:
            index = (index + 1) % self.capacity

        return index

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        return self.hash_table[index].value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            if self.length + 1 >= self.current_max_size:
                self.resize()
                return self.__setitem__(key, value)

            self.length += 1

        self.hash_table[index] = Node(key, value)

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Key not found: {key}")

        self.hash_table[index] = None
        self.length -= 1

    def resize(self) -> None:

        old_hash_table = self.hash_table

        self.__init__(self.capacity * self.capacity_multiplier)

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __str__(self) -> str:
        return str(self.hash_table)

    def __len__(self) -> int:
        return self.length
