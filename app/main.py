from dataclasses import dataclass
from typing import Hashable, Any, Optional, List
from fractions import Fraction


class Dictionary:
    CAPACITY = 8
    INCREASE_MULTIPLIER = 2
    LOAD_FACTOR = Fraction(2, 3)

    @dataclass
    class Node:
        key: Hashable
        value: Any

        def __post_init__(self) -> None:
            self.key_hash = hash(self.key)

    def __init__(self) -> None:
        self.capacity: int = self.CAPACITY
        self.size: int = 0
        self.buckets: List[Optional[Dictionary.Node]] = [None] * self.capacity

    def calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (
            self.buckets[index] is not None
            and self.buckets[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    def resize(self, use_multiplier: bool = True) -> None:
        old_buckets = self.buckets
        if use_multiplier:
            self.capacity *= self.INCREASE_MULTIPLIER
        self.buckets = [None] * self.capacity
        self.size = 0

        for node in old_buckets:
            if node is not None:
                self.__setitem__(node.key, node.value)

    @property
    def max_size(self) -> int:
        return int(self.capacity * self.LOAD_FACTOR)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.max_size:
            self.resize()

        index = self.calculate_index(key)
        if self.buckets[index] is None:
            self.size += 1
        self.buckets[index] = self.Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.calculate_index(key)

        if self.buckets[index] is None:
            raise KeyError(f"Can't find element with key {key}")

        return self.buckets[index].value

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index = self.calculate_index(key)

        if self.buckets[index] is None:
            raise KeyError(f"Can't find element with key {key}")

        self.buckets[index] = None
        self.size -= 1

        if self.size <= self.max_size // self.INCREASE_MULTIPLIER:
            self.resize(use_multiplier=False)

    def rehash(self) -> None:
        self.resize(use_multiplier=False)
