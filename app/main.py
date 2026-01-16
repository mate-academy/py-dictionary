from dataclasses import dataclass
from typing import Optional, Any, List


@dataclass
class Node:
    key: Any
    value: Any
    hash_value: int
    next: Optional["Node"] = None # noqa


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = load_factor
        self.table: List[Optional[Node]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        node_hash = hash(key)
        index = self._hash(node_hash)
        current_node = self.table[index]

        if current_node is None:
            self.table[index] = Node(key, value, node_hash)
            self.size += 1
        else:
            while current_node:
                if current_node.key == key:
                    current_node.value = value
                    return
                if current_node.next is None:
                    current_node.next = Node(key, value, node_hash)
                    self.size += 1
                    break
                current_node = current_node.next

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        node_hash = hash(key)
        index = self._hash(node_hash)
        current_node = self.table[index]

        while current_node:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def _hash(self, node_hash: int) -> int:
        return node_hash % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for current_node in old_table:
            while current_node:
                self[current_node.key] = current_node.value
                current_node = current_node.next

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        node_hash = hash(key)
        index = self._hash(node_hash)
        current_node = self.table[index]
        prev_node = None

        while current_node:
            if current_node.key == key:
                if prev_node is None:
                    self.table[index] = current_node.next
                else:
                    prev_node.next = current_node.next
                self.size -= 1
                return
            prev_node = current_node
            current_node = current_node.next

        raise KeyError(f"Key '{key}' not found")

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        node_hash = hash(key)
        index = self._hash(node_hash)
        current_node = self.table[index]
        prev_node = None

        while current_node:
            if current_node.key == key:
                value = current_node.value
                if prev_node is None:
                    self.table[index] = current_node.next
                else:
                    prev_node.next = current_node.next
                self.size -= 1
                return value
            prev_node = current_node
            current_node = current_node.next

        if default is not None:
            return default

        raise KeyError(f"Key '{key}' not found")

    def update(self, other: dict) -> None: # noqa
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> None:
        for node in self.table:
            current_node = node
            while current_node:
                yield current_node.key
                current_node = current_node.next
