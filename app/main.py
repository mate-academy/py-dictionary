from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity
        self.length = 0

    def _resize(self) -> None:
        if self.length >= self.capacity * self.load_factor:
            self.capacity *= 2
            hash_table_copy = self.hash_table.copy()
            self.hash_table: list = [None] * self.capacity
            self.length = 0

            for node in hash_table_copy:
                if node:
                    self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._resize()
        hashed_key = hash(key)
        position_in_hash_table = hashed_key % self.capacity
        node = self.hash_table[position_in_hash_table]

        while node:
            if node.key == key and node.hashed_key == hash(key):
                node.value = value
                return
            else:
                position_in_hash_table = ((position_in_hash_table + 1)
                                          % self.capacity)
                node = self.hash_table[position_in_hash_table]

        self.hash_table[position_in_hash_table] = Node(key, hashed_key, value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> None:
        hashed_key = hash(key)
        position_in_hash_table = hashed_key % self.capacity
        node = self.hash_table[position_in_hash_table]

        while node:
            if node.key == key and node.hashed_key == hashed_key:
                return node.value
            else:
                position_in_hash_table = ((position_in_hash_table + 1)
                                          % self.capacity)
                node = self.hash_table[position_in_hash_table]
        raise KeyError

    def __len__(self) -> int:
        return self.length


class Node:
    def __init__(self, key: Any, hashed_key: Any, value: Any) -> None:
        self.key = key
        self.hashed_key = hashed_key
        self.value = value
