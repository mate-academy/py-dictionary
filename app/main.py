import math

from typing import Any, Hashable, Iterator
from dataclasses import dataclass


@dataclass
class Node:
    key: Hashable
    value: Any
    hash_value: int


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.capacity = 8
        self.load_factor = 2 / 3
        self.threshold = 5

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if self.length < self.threshold:
            hash_value = self.hash_for_key(key)

            new_node = Node(
                key=key,
                value=value,
                hash_value=hash_value
            )

            table_index = int(hash_value % self.capacity)

            if self.hash_table[table_index] is None:
                self.hash_table[table_index] = new_node
                self.length += 1
                return

            if self.hash_table[table_index].key == key:
                self.hash_table[table_index].value = value
                return

            new_index = self.find_empty_slot(self.hash_table, table_index, key)
            self.hash_table[new_index] = new_node

        else:
            self.resize_hash_table(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        table_index = int(self.hash_for_key(key) % self.capacity)
        if self.hash_table[table_index]:
            if self.hash_table[table_index].key == key:
                return self.hash_table[table_index].value

            next_index = self.find_index_for_same_hash(table_index, key)

            return self.hash_table[next_index].value
        raise KeyError

    def __delitem__(self, key: Hashable) -> None:
        table_index = int(self.hash_for_key(key) % self.capacity)
        if self.hash_table[table_index]:
            if self.hash_table[table_index].key == key:
                self.hash_table[table_index] = None
                self.length -= 1
                return

        next_index = self.find_index_for_same_hash(table_index, key)
        self.hash_table[next_index] = None
        self.length -= 1

    def __iter__(self) -> Iterator:
        hash_table_without_none = []
        for node in self.hash_table:
            if node:
                hash_table_without_none.append((node.key, node.value))

        return iter(hash_table_without_none)

    def get(self, key: Hashable) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: Hashable) -> Any:
        table_index = int(self.hash_for_key(key) * self.capacity)
        if self.hash_table[table_index]:
            value = self.hash_table[table_index].value
            self.__delitem__(key)

            return value
        raise KeyError

    def update(self, key: Hashable, value: Any) -> None:
        table_index = int(self.hash_for_key(key) * self.capacity)
        self.hash_table[table_index].value = value

    def find_index_for_same_hash(self, curr_index: int, key: Hashable) -> int:
        """Return hash_table_index in case when we have collision."""

        for i in range(curr_index + 1, len(self.hash_table)):
            if self.hash_table[i] is None:
                continue
            if self.hash_table[i].key == key:
                return i

        for i in range(curr_index):
            if self.hash_table[i] is None:
                continue
            if self.hash_table[i].key == key:
                return i

        raise KeyError

    def find_empty_slot(
            self,
            hash_table: list,
            curr_index: int,
            key: Hashable = None,
            resize: bool = False
    ) -> int:
        """Find empty slot in hash table for new key
        and find index for key that already exists"""

        table_length = len(hash_table)
        for i in range(curr_index + 1, table_length):
            if hash_table[i] is None:
                if not resize:
                    self.length += 1
                return i
            if hash_table[i].key == key:
                return i

        for i in range(curr_index):
            if hash_table[i] is None:
                if not resize:
                    self.length += 1
                return i
            if hash_table[i].key == key:
                return i

    def resize_hash_table(self, key: Hashable, value: Any) -> None:
        """Resize hash table and call 'self.__setitem__' """

        self.capacity *= 2
        self.threshold = math.floor(self.capacity * self.load_factor)

        new_hash_table = [None] * self.capacity
        for node in self.hash_table:
            if node:
                table_index = int(node.hash_value % self.capacity)
                if new_hash_table[table_index] is None:
                    new_hash_table[table_index] = node
                    continue
                new_index = self.find_empty_slot(
                    hash_table=new_hash_table,
                    curr_index=table_index,
                    key=key,
                    resize=True
                )
                new_hash_table[new_index] = node

        self.hash_table = new_hash_table
        self.__setitem__(key, value)

    @staticmethod
    def hash_for_key(key: Hashable) -> int:
        hash_value = 0
        if isinstance(key, int | float):
            return key

        if isinstance(key, str):
            for char in key:
                hash_value += ord(char)
            return hash_value

        return key.__hash__()

    def clear(self) -> None:
        new_hash_table = [None] * self.capacity
        self.hash_table = new_hash_table
        self.length = 0
