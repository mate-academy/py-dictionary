from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    key: object
    hash_: object
    value: object


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.load_factor = 2 / 3
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity

    def get_cell(self, key: object) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        current_nodes = [node for node in self.hash_table if node]
        self.capacity *= 2
        self.clear()
        for node in current_nodes:
            self.__setitem__(node.key, node.value)

    def get(self, key: object) -> None | object:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: object) -> Node:
        result = self.__getitem__(key)
        self.__delitem__(key)
        return result

    def clear(self) -> None:
        self.size = 0
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: object, value: object) -> None:
        cell = self.get_cell(key)
        while node := self.hash_table[cell]:
            if node.key == key:
                node.value = value
                return
            cell += 1
            if cell == self.capacity:
                cell = 0

        self.hash_table[cell] = Node(
            key,
            hash(key),
            value
        )
        self.size += 1
        if self.size == round(self.capacity * self.load_factor):
            self.resize()

    def __getitem__(self, key: object) -> object:
        cell = self.get_cell(key)
        if not self.hash_table[cell]:
            raise KeyError("This key wasn't found")
        while node := self.hash_table[cell]:
            if node.key == key:
                return node.value
            cell += 1
            if cell == self.capacity:
                cell = 0

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: object) -> None:
        cell = self.get_cell(key)
        while node := self.hash_table[cell]:
            if node.key == key:
                node_index = self.hash_table.index(node)
                self.hash_table[node_index] = None
                self.size -= 1
                return
            cell += 1
            if cell == self.capacity:
                cell = 0

    def __iter__(self) -> Iterator:
        return iter(self.hash_table)
