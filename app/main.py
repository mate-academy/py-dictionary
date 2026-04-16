import dataclasses
from typing import Any, List, Optional


@dataclasses.dataclass
class Node:
    key: Any
    hash_value: int
    value: Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR_THRESHOLD = 2 / 3

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._size = 0
        self._table: List[Optional[Node]] = [None] * self._capacity

    def _get_index(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._size = 0
        self._table = [None] * self._capacity

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size / self._capacity >= self.LOAD_FACTOR_THRESHOLD:
            self._resize()

        hash_value = hash(key)
        index = self._get_index(key)

        # Manejo de colisiones mediante Linear Probing (Sondeo Lineal)
        while self._table[index] is not None:
            if self._table[index].key == key:
                self._table[index].value = value
                return
            index = (index + 1) % self._capacity

        self._table[index] = Node(key, hash_value, value)
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._get_index(key)
        start_index = index

        while self._table[index] is not None:
            if self._table[index].key == key:
                return self._table[index].value
            index = (index + 1) % self._capacity
            if index == start_index:  # Hemos dado la vuelta completa
                break

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self._size
