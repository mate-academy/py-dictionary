from fractions import Fraction
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity
        self.load_factor = Fraction(2, 3)

    def _calculate_index(self, key: Hashable) -> tuple[int, int]:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index, key_hash

    def rebuild(self) -> None:
        previous_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in previous_table:
            if node is not None:
                index = node.key_hash % self.capacity
                while self.hash_table[index] is not None:
                    index = (index + 1) % self.capacity
                self.hash_table[index] = node
                self.size += 1

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index, key_hash = self._calculate_index(key)

        if self.hash_table[index] is None:
            if self.size + 1 > int(self.capacity * self.load_factor):
                self.rebuild()
                return self.__setitem__(key, value)
            self.size += 1
        self.hash_table[index] = Dictionary.Node(key, key_hash, value)

    def __getitem__(self, key: Hashable) -> Any:
        index, _ = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Unknown key: {key}")

        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.size

    class Node:
        def __init__(self, key: Hashable, key_hash: int, value: Any) -> None:
            self.key = key
            self.key_hash = key_hash
            self.value = value
