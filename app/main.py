from dataclasses import dataclass
from typing import Any, Hashable


CAPACITY = 8
LOAD_FACTOR = 2 / 3
CAPACITY_MULTIPLY = 2


@dataclass
class Node:
    key: Hashable
    key_hash: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = CAPACITY
        self.hash_table: list[None | Node] = [None] * CAPACITY

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.set_node_to_hash_table(key, value, self.hash_table)

        if self.length >= int(self.capacity * LOAD_FACTOR):
            self.resize()

    def set_node_to_hash_table(
            self,
            key: Hashable,
            value: Any,
            hash_table: list[Node | None],
    ) -> None:
        key_hash = hash(key)
        hash_index = key_hash % self.capacity

        while hash_table[hash_index]:
            if hash_table[hash_index].key == key:
                hash_table[hash_index].value = value
                return

            hash_index = (hash_index + 1) % self.capacity

        hash_table[hash_index] = Node(key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        hash_index = hash_key % self.capacity

        while (
                self.hash_table[hash_index]
                and self.hash_table[hash_index].key != key
        ):
            hash_index = (hash_index + 1) % self.capacity

        if not self.hash_table[hash_index]:
            raise KeyError(f"Key {key} doesn't exist")

        return self.hash_table[hash_index].value

    def resize(self) -> None:
        self.length = 0
        self.capacity *= CAPACITY_MULTIPLY
        old_hash_table = [
            item
            for item in self.hash_table
            if item
        ]
        self.hash_table = [None] * self.capacity

        for item in old_hash_table:
            self.__setitem__(item.key, item.value)
