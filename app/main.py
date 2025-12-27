from dataclasses import dataclass
from typing import Hashable, Any


class Dictionary:
    INITIAL_CAPACITY = 8
    RESIZE_THRESHOLD = 2 / 3

    @dataclass
    class Bucket:
        key: Hashable
        value: Any

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self._capacity = capacity
        self._size = 0
        self._table: list[Dictionary.Bucket | None] = [None] * self._capacity

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity

        while self._table[index] is not None and self._table[index].key != key:
            index = (index + 1) % self._capacity

        return index

    @property
    def current_max_size(self) -> float | int:
        return self._capacity * Dictionary.RESIZE_THRESHOLD

    def resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self._table[index] is None:
            if self._size + 1 >= self.current_max_size:
                self.resize()
                index = self._calculate_index(key)

            self._size += 1

        self._table[index] = Dictionary.Bucket(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if self._table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        return self._table[index].value

    def __len__(self) -> int:
        return self._size
