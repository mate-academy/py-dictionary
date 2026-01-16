from collections.abc import Hashable
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._load_factor = 2 / 3
        self._size = 0
        self.nodes = [None] * self._capacity

    def _resize(self) -> None:
        new_capacity = self._capacity * 2
        new_nodes = [None] * new_capacity
        for node in self.nodes:
            if node is not None:
                key, value = node
                index: int = hash(key) % new_capacity
                while new_nodes[index] is not None:
                    index = (index + 1) % new_capacity
                new_nodes[index] = (key, value)
        self._capacity = new_capacity
        self.nodes = new_nodes

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._size / self._capacity >= self._load_factor:
            self._resize()

        index = hash(key) % self._capacity
        while self.nodes[index] is not None:
            existing_key, _ = self.nodes[index]
            if existing_key == key:
                self.nodes[index] = (key, value)
                return
            index = (index + 1) % self._capacity
        self.nodes[index] = (key, value)
        self._size += 1

    def __getitem__(self, item: Hashable) -> Any:
        index = hash(item) % self._capacity
        start_index = index

        while self.nodes[index] is not None:
            key, value = self.nodes[index]
            if key == item:
                return value
            index = (index + 1) % self._capacity
            if index == start_index:
                break
        raise KeyError(f"Key {item} not found")

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self.nodes = [None] * self._capacity
        self._size = 0

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self._capacity
        start_index = index

        while self.nodes[index] is not None:
            existing_key, _ = self.nodes[index]
            if existing_key == key:
                self.nodes[index] = None
                self._size -= 1
                return
            index = (index + 1) % self._capacity
            if index == start_index:
                break
        raise KeyError(f"Key {key} not found")

    def __iter__(self) -> iter:
        for node in self.nodes:
            if node is not None:
                yield node[0]

    def get(self, key: Hashable, value: Any = 0) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return value

    def pop(self, key: Hashable) -> Any:
        index = hash(key) % self._capacity
        start_index = index
        while self.nodes[index] is not None:
            node_key, node_value = self.nodes[index]
            if node_key == key:
                self.nodes[index] = None
                self._size -= 1
                return node_value
            index = (index + 1) % self._capacity
            if index == start_index:
                break
        raise KeyError(f"Key {key} not found")

    def update(self, key: Hashable, value: Any) -> None:
        self.__setitem__(key, value)
