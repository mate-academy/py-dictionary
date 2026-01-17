from dataclasses import dataclass
from typing import Hashable, Any, Union


@dataclass
class Node:
    hash_: int
    key: Hashable
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.load_factor = 2 / 3
        self.hash_table: list[Union[None, Node]] = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.find_index(key)
        self.add_items(index, key, value)
        if self.hash_table_is_overloaded():
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.find_index(key)
        self.check_key_exists(index, key)
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.length

    def find_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self.capacity

        while (
                self.hash_table[index] is not None
                and (
                    self.hash_table[index].hash_ != hash_
                    or self.hash_table[index].key != key
                )
        ):
            index += 1
            index %= self.capacity

        return index

    def add_items(
            self,
            index: int,
            key: Hashable,
            value: Any
    ) -> None:
        if self.hash_table[index] is None:
            self.length += 1
        self.hash_table[index] = Node(hash(key), key, value)

    def hash_table_is_overloaded(self) -> bool:
        return self.length >= self.capacity * self.load_factor

    def resize(self) -> None:
        self.capacity *= 2
        self.length = 0
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.capacity

        for items in old_hash_table:
            if items is not None:
                self[items.key] = items.value

    def check_key_exists(self, index: int, key: Hashable) -> None:
        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} not found")
