from typing import Any, Iterator
from dataclasses import dataclass


@dataclass
class Node:
    key: Any
    _hash: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity


    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._hash(key)
        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = Node(key, hash(key), value)
        self.length += 1

        if self.length + 1 >= self.capacity * self.load_factor:
            self.resize_dictionary()


    def resize_dictionary(self) -> None:
        old_hash_table = [item for item in self.hash_table if item]
        self.hash_table = (len(self.hash_table) * 2) * [None]
        self.capacity *= 2
        self.length = 0
        for item in old_hash_table:
            self.__setitem__(item.key, item.value)

    def check_valid_index(self, key: Any) -> int:
        index = self._hash(key)
        while self.hash_table[index]:
            if self.hash_table[index].key == key:
                return index
            index = (index + 1) % self.capacity
        raise KeyError("Key not found in dictionary")

    def __getitem__(self, key: Any) -> Any:
        index = self.check_valid_index(key)
        return self.hash_table[index].value

    def __delitem__(self, key: Any) -> None:
        index = self.check_valid_index(key)
        self.hash_table[index] = None
        self.length -= 1

    def clear(self) -> None:
        self.length = 0
        self.hash_table = self.capacity * [None]

    def get(self, key: Any) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            print("Key not found in dictionary")
            return None

    def pop(self, key: Any) -> Any:
        index = self.check_valid_index(key)
        value = self.hash_table[index].value

        self.hash_table[index] = None
        self.length -= 1

        return value

    def update(self, key: Any, value: Any) -> None:
        self.__setitem__(key, value)

    def __iter__(self) -> Iterator:
        for node in self.hash_table:
            if node is not None:
                yield node.key, node.value
