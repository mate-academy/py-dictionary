from dataclasses import dataclass, field
from typing import Any, Hashable


@dataclass(slots=True)
class Node:
    key: Hashable
    value: Any
    hash_: int = field(init=False)

    def __post_init__(self) -> None:
        self.hash_ = hash(self.key)


class Dictionary:
    LOAD_FACTOR = 2 / 3
    INITIAL_CAPACITY = 8
    CAPACITY_MULTIPLIER = 2

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._hash_table: list[None | Node] = [None] * self._capacity
        self._size = 0

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self._capacity

    def _calculate_index(self, key: Hashable) -> int:
        hash_value = hash(key)
        mask = self._capacity - 1
        index = hash_value & mask
        while (
                (node := self._hash_table[index]) is not None
                and (node.hash_ != hash_value
                     or node.key != key)
        ):
            index = self._linear_probing(index)
        return index

    @property
    def _threshold(self) -> float:
        return self._capacity * self.LOAD_FACTOR

    def _need_resize(self) -> bool:
        return self._size + 1 > self._threshold

    def _resize(self) -> None:
        print("RESIZE CALLED !")
        old_table = self._hash_table
        self._capacity *= self.CAPACITY_MULTIPLIER
        self._size = 0
        self._hash_table = [None] * self._capacity
        for node in old_table:
            if node:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> int | None:
        index = self._calculate_index(key)
        if (node := self._hash_table[index]) is not None:
            node.value = value
        else:
            if self._need_resize():
                self._resize()
                self[key] = value
                return
            self._size += 1
            self._hash_table[index] = Node(key=key, value=value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        if (node := self._hash_table[index]) is None:
            raise KeyError(f"Key: {key} not found")
        return node.value

    def __len__(self) -> int:
        return self._size


if __name__ == "__main__":
    d = Dictionary()
