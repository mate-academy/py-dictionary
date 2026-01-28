import dataclasses
from typing import Hashable, Any


INITIAL_CAPACITY = 8
RESIZE_TRESHOLD = 2 / 3
CAPACITY_MULTIPLAYER = 2


@dataclasses.dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table: list[Node | None] = [None] * self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    @property
    def current_max_size(self) -> float:
        return self.capacity * RESIZE_TRESHOLD

    def resize(self) -> None:
        old_hash_table = self.hash_table

        self.capacity *= CAPACITY_MULTIPLAYER
        self.size = 0
        self.hash_table: list[Node | None] = [None] * self.capacity

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            if self.size + 1 >= self.current_max_size:
                self.resize()
                return self.__setitem__(key, value)
            self.size += 1
        self.hash_table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")
        return self.hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        self.hash_table[index] = None
        self.size -= 1

    def get(self, key: Hashable, default: Any = None) -> None:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int | float:
        return self.size

    def __str__(self) -> str:
        return str(self.hash_table)
