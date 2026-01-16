import copy
from typing import Any
import dataclasses
# from point import Point


class Dictionary:
    @dataclasses.dataclass
    class Node:
        key: Any
        hash_: int
        value: Any

    DEFAULT_CAPACITY: int = 8
    capacity: int = DEFAULT_CAPACITY
    load_factor = 2 / 3
    size: int = 0

    def __init__(self) -> None:
        self.list_nodes = [None] * self.DEFAULT_CAPACITY

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, key: Any) -> Any:
        index_num = hash(key) % self.capacity
        nodes = self.list_nodes[index_num]
        if nodes is None:
            raise KeyError
        else:
            for node in nodes:
                if node.key == key:
                    return node.value
            raise KeyError(f"{key} is not existed...")

    def resize(self) -> None:
        if self.size < int(self.load_factor * self.capacity):
            return
        self.capacity *= 2
        old_list_nodes = copy.copy(self.list_nodes)
        self.list_nodes = [None] * self.capacity
        for nodes in old_list_nodes:
            if nodes is None:
                continue
            for node in nodes:
                self.simply_setitem(node.key, node.value)

    def simply_setitem(self, key: Any, value: Any) -> None:
        index_num = hash(key) % self.capacity
        nodes = self.list_nodes[index_num]
        node = self.Node(key, hash(key), value)
        if nodes is None:
            self.list_nodes[index_num] = []
            self.list_nodes[index_num].append(node)
            self.size += 1
        else:
            for item in nodes:
                if item.key == key:
                    item.value = value
                    return
            nodes.append(node)
            self.size += 1

    def __setitem__(self, key: Any, value: Any) -> None:
        self.simply_setitem(key, value)
        self.resize()
