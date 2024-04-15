from typing import Any, Hashable
from random import randint


class Node:
    def __init__(self, key: Hashable, hash_: int, value: Any) -> None:
        self.key = key
        self.hash_ = hash_
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.length = 0
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        node = self.hash_table[index]
        while node:
            if node.key == key:
                node.value = value
                return
            if node.next:
                index = node.next
                node = self.hash_table[node.next]
                continue
            while True:
                new_index = randint(0, self.capacity - 1)
                if not self.hash_table[new_index]:
                    node.next = new_index
                    self.hash_table[index] = node
                    break

        self.hash_table[index] = Node(key=key, value=value, hash_=key_hash)
        self.length += 1

        if self.length >= self.capacity * self.load_factor:
            self.__resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        node = self.hash_table[index]
        while node:
            if node.key == key:
                return node.value
            if node.next:
                node = self.hash_table[node.next]
                continue
            break
        raise KeyError(f"Key: {key} not found!")

    def __resize(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table.copy()
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_hash_table:
            if node:
                self.__setitem__(node.key, node.value)
