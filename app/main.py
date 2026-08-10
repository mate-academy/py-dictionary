from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    key: Any
    key_hash: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.nodes: list[Node | None] = [None] * self.capacity
        self.length = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        node_hash = hash(key)
        index = node_hash % self.capacity
        for _ in range(self.capacity):
            if self.nodes[index] is None:
                break
            if self.nodes[index].key == key:
                self.nodes[index].value = value
                return
            index = (index + 1) % self.capacity

        if self.length >= self.capacity * self.load_factor:
            self.increase_size()

        self.add_node_in_list(Node(key, node_hash, value))

    def __getitem__(self, key: Any) -> Any:
        index = self.find_index(key)
        return self.nodes[index].value

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Any) -> None:
        index = self.find_index(key)

        self.nodes[index] = None
        self.length -= 1

        index = (index + 1) % self.capacity

        while self.nodes[index] is not None:
            node = self.nodes[index]

            self.nodes[index] = None
            self.length -= 1

            self.add_node_in_list(node)

            index = (index + 1) % self.capacity

    def find_index(self, key: Any) -> int:
        key_hash = hash(key)
        index = key_hash % self.capacity

        for _ in range(self.capacity):
            if self.nodes[index] is None:
                raise KeyError(f"Key '{key}' not found in Dictionary")

            if self.nodes[index].key == key:
                return index

            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found in Dictionary")

    def increase_size(self) -> None:
        self.capacity *= 2
        previous_nodes = self.nodes
        self.nodes = [None] * self.capacity
        self.length = 0

        for node in previous_nodes:
            if node:
                self.add_node_in_list(node)

    def add_node_in_list(self, node: Node) -> None:
        index = node.key_hash % self.capacity

        while self.nodes[index]:
            index = (index + 1) % self.capacity

        self.nodes[index] = node
        self.length += 1
