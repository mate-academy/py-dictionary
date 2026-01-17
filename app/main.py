from fractions import Fraction
from typing import Any, Hashable


class Dictionary:
    class Node:
        def __init__(self, key: Hashable, value: Any) -> None:
            self.key = key
            self.value = value

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor_threshold = Fraction(2, 3)
        self.hash_table: list[Dictionary.Node | None] = [None] * self.capacity

    def calculate_hash(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    @property
    def current_max_size(self) -> int:
        return int(self.capacity * self.load_factor_threshold)

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor_threshold:
            self.resize()

        index = self.calculate_hash(key)

        if self.hash_table[index] is None:
            self.size += 1

        self.hash_table[index] = Dictionary.Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.calculate_hash(key)
        if self.hash_table[index] is None:
            raise KeyError(f"No value for key: {key}")
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Hashable) -> None:
        index = self.calculate_hash(key)
        if self.hash_table[index] is None:
            raise KeyError(f"No value for key: {key}")

        self.hash_table[index] = None
        self.size -= 1

        for values in self.hash_table:
            if values is not None:
                self.__setitem__(values.key, values.value)
