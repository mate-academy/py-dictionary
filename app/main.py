from __future__ import annotations
from dataclasses import dataclass
from typing import Hashable, Any, Union, Iterator


@dataclass
class Node:
    node_key: Hashable
    node_hash: int
    node_value: Any


# singleton
DELETED = object()
SENTINEL = object()


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.load_factor: float = 2 / 3
        self.threshold: int = int(self.capacity * self.load_factor)
        self.size: int = 0
        self.nodes: list[Node | None] = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.threshold:
            self.capacity *= 2
            self.threshold = int(self.capacity * self.load_factor)
            new_nodes = [None] * self.capacity
            for node in self.nodes:
                if node is not None and node is not DELETED:
                    self.__add_node(new_nodes, node)
            self.nodes = new_nodes
        new_node = Node(key, hash(key), value)
        if self.__add_node(self.nodes, new_node):
            self.size += 1

    def __add_node(
            self,
            nodes: list[Union[Node, None, object]],
            node: Union[Node, None, object]
    ) -> bool:
        """ True = new item inserted; False: = updated / ignored"""

        if node is None or node is DELETED:
            return False

        slot = node.node_hash % len(nodes)

        if nodes[slot] is None or nodes[slot] is DELETED:
            nodes[slot] = node
            return True
        if (node.node_hash == nodes[slot].node_hash
                and node.node_key == nodes[slot].node_key):
            nodes[slot].node_value = node.node_value
            return False
        if nodes[slot].node_key != node.node_key:
            new_slot = (slot + 1) % len(nodes)
            for _ in range(len(nodes)):
                if (nodes[new_slot] is None
                        or nodes[new_slot] is DELETED):
                    nodes[new_slot] = node
                    return True
                # overwrite the old value
                if (nodes[new_slot].node_hash == node.node_hash
                        and nodes[new_slot].node_key == node.node_key):
                    nodes[new_slot].node_value = node.node_value
                    return False

                new_slot = (new_slot + 1) % len(nodes)
            else:
                raise Exception(f"Size: {len(nodes)} no empty slots found")
        return False

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        slot = key_hash % self.capacity

        for _ in range(self.capacity):
            if self.nodes[slot] is None:
                raise KeyError(f"{key} is not found in dictionary")
            if self.nodes[slot] is DELETED:
                slot = (slot + 1) % self.capacity
                continue
            if (self.nodes[slot].node_hash == key_hash
                    and self.nodes[slot].node_key == key):
                return self.nodes[slot].node_value
            slot = (slot + 1) % self.capacity
        raise KeyError(f"{key} is not found in dictionary")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.size = 0
        self.capacity = 8
        self.threshold = int(self.capacity * self.load_factor)
        self.nodes = [None] * self.capacity

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        slot = key_hash % self.capacity

        for _ in range(self.capacity):
            if self.nodes[slot] is None:
                raise KeyError(f"{key} is not found in dictionary")
            if self.nodes[slot] is DELETED:
                slot = (slot + 1) % self.capacity
                continue
            if (self.nodes[slot].node_hash == key_hash
                    and self.nodes[slot].node_key == key):
                self.nodes[slot] = DELETED
                self.size -= 1
                break
            slot = (slot + 1) % self.capacity
        else:
            raise KeyError(f"{key} is not found in dictionary")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = SENTINEL) -> Any:
        value = self.get(key, SENTINEL)
        if value is SENTINEL:
            if default is SENTINEL:
                raise KeyError(f"{key} is not found")
            else:
                return default
        else:
            self.__delitem__(key)
            return value

    def __iter__(self) -> Iterator[Hashable]:
        return (
            node.node_key
            for node in self.nodes
            if node is not None and node is not DELETED
        )

    def update(self, other: Dictionary) -> None:
        for other_key in other:
            self.__setitem__(other_key, other.get(other_key))
