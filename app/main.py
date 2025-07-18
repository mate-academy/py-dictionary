import math
from typing import Any

from app.Node import Node


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.load_factor: float = 2 / 3
        self.max_elements: int = math.floor(self.capacity * self.load_factor)

        self.hash_map: list[Any] = [None] * self.capacity
        self.count_of_elements: int = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.count_of_elements + 1) > self.max_elements:
            self._resize_hashmap()
        self.put_element_in_hash_map(key, value)

    def __getitem__(self, key: Any) -> Any:
        hash_code = hash(key)
        index = hash_code % self.capacity

        while True:
            node = self.hash_map[index]

            if node is None:
                raise KeyError(f"Key {key} not found")

            if node.hash_code == hash_code and node.key == key:
                return node.value
            else:
                index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return sum(1 for node in self.hash_map if isinstance(node, Node))

    def _resize_hashmap(self) -> None:
        self.capacity *= 2
        self.max_elements = math.floor(self.capacity * self.load_factor)

        current_hash = self.hash_map
        self.hash_map = [None] * self.capacity

        for node in current_hash:
            if isinstance(node, Node):
                self.put_element_in_hash_map(node.key, node.value)

    def put_element_in_hash_map(self, key: Any, value: Any) -> None:
        node = Node(key, hash(key), value)
        index = node.hash_code % self.capacity
        is_update = False

        while True:
            if isinstance(self.hash_map[index], Node):
                current_node = self.hash_map[index]

                if (node.hash_code == current_node.hash_code) and (
                    node.key == current_node.key
                ):
                    current_node.value = value
                    is_update = True
                    break
                else:
                    index = (index + 1) % self.capacity
                    continue
            break

        if not is_update:
            self.hash_map[index] = node
            self.count_of_elements += 1
