from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.table: list[Node | None] = [None] * capacity
        self.size = 0
        self.load_factor = 2 / 3

    @property
    def max_size(self) -> float:
        return self.load_factor * self.capacity

    def _get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
            self.table[index] is not None
            and self.table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)

        if self.table[index] is None:
            if self.size + 1 >= self.max_size:
                self.resize()
                return self.__setitem__(key, value)

            self.size += 1

        self.table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)

        if self.table[index] is None:
            raise KeyError(f"{key}: such a kay does not exist")

        return self.table[index].value

    def resize(self) -> None:
        old_table = self.table

        self.__init__(self.capacity * 2)

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __len__(self) -> int:
        return self.size
