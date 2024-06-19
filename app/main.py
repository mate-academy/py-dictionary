from __future__ import annotations
from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, hash_key: int, value: Any) -> None:
        self.key = key
        self.hash_key = hash_key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self) -> None:
        self.hash_table = [None] * 8
        self.hash_keys = []
        self.length = 0

    def get_hash_key(self, key: Hashable) -> int:
        for item in self.hash_keys:
            if item[0] == key:
                return item[1]
        new_hash = hash(key)
        self.hash_keys.append((key, new_hash))
        return new_hash

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.check()
        hash_key = self.get_hash_key(key)
        index = hash_key % len(self.hash_table)
        if self.hash_table[index] is None:
            self.length += 1
            self.hash_table[index] = Node(key, hash_key, value)
        elif self.hash_table[index].key == key:
            self.hash_table[index].value = value
        elif self.hash_table[index].key != key:
            current_next = self.hash_table[index]
            while True:
                if current_next.key == key:
                    current_next.value = value
                    break
                if current_next.next is None:
                    self.length += 1
                    current_next.next = Node(key, hash_key, value)
                    break
                current_next = current_next.next

    def check(self) -> None:
        if self.length == int((2 / 3) * len(self.hash_table)):
            self.resize()

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.hash_table = [None] * (len(self.hash_table) * 2)
        self.length = 0
        for node in old_hash_table:
            while node:
                self[node.key] = node.value
                node = node.next

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = self.get_hash_key(key)
        index = hash_key % len(self.hash_table)
        if self.hash_table[index] is None:
            raise KeyError
        if self.hash_table[index].key == key:
            return self.hash_table[index].value
        current_next = self.hash_table[index]
        while current_next:
            if current_next.key == key:
                return current_next.value
            current_next = current_next.next
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        hash_key = self.get_hash_key(key)
        index = hash_key % len(self.hash_table)
        if self.hash_table[index] is None:
            raise KeyError
        node = self.hash_table[index]
        while node:
            node_next = node.next
            if node.key == key and node_next:
                node = node_next
                return
            if node.key == key and node_next is None:
                node = None
                return
            node = node.next

    def __iter__(self) -> DictIterable:
        return DictIterable(self.hash_table)

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            self.__setitem__(key, default_value)
            return self.__getitem__(key)


class DictIterable:
    def __init__(self, hash_table: list[Any]) -> None:
        self.hash_table = hash_table
        self.index = 0

    def __iter__(self) -> DictIterable:
        return self

    def __next__(self) -> Any:
        while (
            self.index < len(self.hash_table)
            and self.hash_table[self.index] is None
        ):
            self.index += 1
        if self.index >= len(self.hash_table):
            raise StopIteration
        node = self.hash_table[self.index]
        if node.next is None:
            self.index += 1
            return node.key
        while node:
            yield node.key
            node = node.next
        self.index += 1
