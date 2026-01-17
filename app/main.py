from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 0.6
        self.length = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = self.get_hash(key)
        index = hash_value % self.capacity

        node = self.table[index]
        while node:
            if node[0] == key:
                node[1] = value
                return
            node = node[2]

        new_node = [key, value, self.table[index]]
        self.table[index] = new_node
        self.length += 1

        if self.length / self.capacity > self.load_factor:
            self.resize_table()

    def __getitem__(self, key: Hashable) -> None:
        hash_value = self.get_hash(key)
        index = hash_value % self.capacity

        node = self.table[index]
        while node:
            if node[0] == key:
                return node[1]
            node = node[2]

        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def get_hash(self, key: Hashable) -> int:
        return hash(key)

    def resize_table(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for node in self.iterate_nodes():
            index = self.get_hash(node[0]) % new_capacity
            new_node = [node[0], node[1], new_table[index]]
            new_table[index] = new_node

        self.capacity = new_capacity
        self.table = new_table

    def iterate_nodes(self) -> None:
        for nodes in self.table:
            node = nodes
            while node:
                yield node
                node = node[2]
