from dataclasses import dataclass
from typing import Any, List, Optional, Hashable


@dataclass
class Node:
    my_hash: int
    key: int
    value: Any


class Dictionary:
    default_size = 8
    load_factor = 2 / 3
    new_size = 2

    def __init__(self) -> None:
        self.hashtable: List[Optional[Node]] = \
            [None] * Dictionary.default_size
        self.size = 0
        self.capacity = Dictionary.default_size

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, item: Any) -> Any:
        hash_ = hash(item)
        index = hash_ % self.capacity
        while self.hashtable[index] is not None:
            if self.hashtable[index].key == item:
                return self.hashtable[index].value
            index = (index + 1) % self.capacity
        raise KeyError

    def resize(self) -> None:
        previous_nodes = [node for node in self.hashtable if node is not None]
        self.capacity *= Dictionary.new_size
        self.hashtable = [None for _ in range(self.capacity)]
        self.size = 0

        for node in previous_nodes:
            self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> Any:
        hash_ = hash(key)
        index = hash_ % self.capacity

        while self.hashtable[index] is not None:
            current_node = self.hashtable[index]

            if hash_ == current_node.my_hash and key == current_node.key:
                current_node.value = value
                return
            index = (index + 1) % self.capacity

        self.hashtable[index] = Node(hash_, key, value)
        self.size += 1

        if (self.size + 1) > Dictionary.load_factor * self.capacity:
            self.resize()
