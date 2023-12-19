from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, hash_num: int, value: Any) -> None:
        self.key = key
        self.hash_num = hash_num
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 0.67
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length >= self.capacity * self.load_factor:
            self.resize()
        hash_index = self.get_index(key)
        while (
                self.hash_table[hash_index]
                and self.hash_table[hash_index].key != key
        ):
            hash_index += 1
            hash_index %= self.capacity

        if self.hash_table[hash_index] is None:
            self.hash_table[hash_index] = Node(key, hash(key), value)
            self.length += 1
        else:
            self.hash_table[hash_index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        hash_index = self.get_index(key)
        while (
                self.hash_table[hash_index]
                and self.hash_table[hash_index].key != key
        ):
            hash_index += 1
            hash_index %= self.capacity

        if self.hash_table[hash_index] is None:
            raise KeyError
        return self.hash_table[hash_index].value

    def get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_hash_table:
            if node:
                self[node.key] = node.value
