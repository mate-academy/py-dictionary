from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.66) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table = [None] * 8

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.resize()
        index = hash(key) % self.capacity
        node = self.hash_table[index]
        while node:
            if node[0] == key:
                node[2] = value
                return
            node = node[3]
        new_node = [key, hash(key), value, self.hash_table[index]]
        self.hash_table[index] = new_node
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        node = self.hash_table[index]
        while node:
            if node[0] == key:
                return node[2]
            node = node[3]
        raise KeyError(f"Key '{key}' not found in the dictionary.")

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        self.capacity *= 2
        new_hash_table = [None] * self.capacity

        for node in self.hash_table:
            while node:
                index = hash(node[0]) % self.capacity
                new_node = [node[0], node[1], node[2], new_hash_table[index]]
                new_hash_table[index] = new_node
                node = node[3]

        self.hash_table = new_hash_table
