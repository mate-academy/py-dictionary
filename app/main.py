from dataclasses import dataclass

from typing import Any


@dataclass
class Node:
    key: Any
    hash_id: int
    value: Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.length = capacity
        self.nodes = [None] * capacity
        self.size = 0
        self.load = int(capacity * 2 / 3)

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_id = hash(key)
        index = hash_id % self.length
        while True:
            if self.nodes[index] is None:
                self.nodes[index] = Node(key, hash_id, value)
                self.size += 1
                self.__check_load__()
                break
            if self.nodes[index].key == key:
                self.nodes[index].value = value
                break
            index = (index + 1) % self.length

    def __check_load__(self) -> None:
        if self.size == self.load:
            self.__resize__(capacity=self.length * 2)

    def __resize__(self, capacity: int) -> None:
        old_nodes = self.nodes
        self.length = capacity
        self.nodes = [None] * capacity
        self.size = 0
        self.load = int(capacity * 2 / 3)
        for node in old_nodes:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __getitem__(self, key: Any) -> Any:
        hash_id = hash(key)
        index = hash_id % self.length
        while self.nodes[index] is not None:
            if self.nodes[index].key == key:
                return self.nodes[index].value
            index = (index + 1) % self.length
        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.length = 8
        self.nodes = [None] * 8
        self.size = 0
        self.load = int(self.length * 2 / 3)

    def __delitem__(self, key: Any) -> None:
        hash_id = hash(key)
        index = hash_id % self.length
        while self.nodes[index] is not None:
            if self.nodes[index].key == key:
                self.nodes[index] = None
                self.size -= 1
                return
            index = (index + 1) % self.length
        raise KeyError(f"Key '{key}' not found.")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        item_for_return = self.__getitem__(key)
        self.__delitem__(key)
        return item_for_return

    def update(self, other_dict: dict[Any, Any]) -> None:
        for key, value in other_dict.items():
            self.__setitem__(key, value)

    def __iter__(self) -> Any:
        for node in self.nodes:
            if node is not None:
                yield node.key
