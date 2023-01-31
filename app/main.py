from typing import Any, Hashable


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor = 2 / 3
        self.threshold = int(self.capacity * self.load_factor)
        self.table = [[] for _ in range(self.capacity)]

    def table_resize(self) -> None:
        hash_table = self.table
        self.capacity *= 2
        self.size = 0
        self.threshold = int(self.capacity * self.load_factor)
        self.table = [[] for _ in range(self.capacity)]

        for node in hash_table:
            if node:
                self[node[0]] = node[2]

    def __getitem__(self, key: Hashable) -> Any:
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        nodes = self.table

        while nodes[index]:
            if nodes[index][0] == key and nodes[index][1] == hashed_key:
                return nodes[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.table_resize()

        hashed_key = hash(key)
        index = hashed_key % self.capacity
        nodes = self.table

        while True:
            if not nodes[index]:
                self.size += 1
                nodes[index] = [key, hashed_key, value]
                break
            if nodes[index][0] == key and nodes[index][1] == hashed_key:
                nodes[index][2] = value
                break
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.size
