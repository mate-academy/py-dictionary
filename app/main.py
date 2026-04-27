import dataclasses
from typing import Hashable, Any


@dataclasses.dataclass()
class Node:
    key: Hashable
    value: Any
    hash_value: int


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3
    CAPACITY_MULTIPLIER = 2
    _DELETED = object()

    def __init__(self) -> None:
        self.hash_table: list[Node | None] = [None] * self.INITIAL_CAPACITY
        self.length = 0
        self._capacity = self.INITIAL_CAPACITY

    @property
    def _threshold(self) -> float:
        return self._capacity * self.LOAD_FACTOR

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self._capacity

    def _calculate_index(self, key: Hashable) -> int:
        hash_value = hash(key)
        index = hash_value % self._capacity

        while (
            (node := self.hash_table[index]) is not None
            and (node.hash_value != hash_value or node.key != key)
        ):
            index = self._linear_probing(index)

        return index

    def _resize(self) -> None:
        old_table = self.hash_table

        self._capacity *= self.CAPACITY_MULTIPLIER
        self.hash_table = [None] * self._capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self._capacity

        while (
            (node := self.hash_table[index]) is not None
            and (node.hash_value != hash_value or node.key != key)
        ):
            index = self._linear_probing(index)

        if self.hash_table[index] is None:
            self.hash_table[index] = Node(key, value, hash_value)
            self.length += 1
        else:
            self.hash_table[index].value = value

        if self.length >= self._threshold:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index = hash_value % self._capacity

        while (
                (node := self.hash_table[index]) is not None
        ):
            if node.key == key:
                return node.value
            index = self._linear_probing(index)

        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = hash_value % self._capacity

        while (node := self.hash_table[index]) is not None:
            if node is not self._DELETED and node.key == key:
                self.hash_table[index] = self._DELETED
                self.length -= 1
                return
            index = self._linear_probing(index)

        raise KeyError(key)
