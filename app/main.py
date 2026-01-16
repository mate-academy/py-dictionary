from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
                self.hash_table[index] is not None
                and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    def current_max_size(self, threshold: float = 2 / 3) -> float:
        return self.capacity * threshold

    def resize(self, capacity_multiplier: int = 2) -> None:
        previous_hash_table = self.hash_table

        self.__init__(self.capacity * capacity_multiplier)

        for node in previous_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.calculate_index(key)

        if self.hash_table[index] is None:
            if self.size + 1 >= self.current_max_size():
                self.resize()
                return self.__setitem__(key, value)

            self.size += 1

        self.hash_table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value key: {key}")

        return self.hash_table[index].value

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Hashable) -> None:
        index = self.calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        self.hash_table[index] = None
        self.size -= 1

    def __len__(self) -> int:
        return self.size

    def pop(self, key: Hashable) -> Any:
        index = self.calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Cannot find value for key: {key}")

        value = self.hash_table[index].value
        self.hash_table[index] = None
        self.size -= 1

        return value
