from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any,
                 next_node: ("Node", None) = None) -> None:
        self.key = key
        self.value = value
        self.next_node = next_node


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.66) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = Node(key, value)

        else:
            current = self.table[index]
            while current is not None:
                if current.key == key and hash(current.key) == hash(key):
                    current.value = value
                    return
                if current.next_node is None:
                    break
                current = current.next_node
            current.next_node = Node(key, value)
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._hash(key)
        current = self.table[index]
        while current is not None:
            if current.key == key and hash(current.key) == hash(key):
                return current.value
            current = current.next_node

        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        index = self._hash(key)
        current = self.table[index]
        prev_node = None

        while current is not None:
            if current.key == key:
                if prev_node:
                    prev_node.next_node = current.next_node
                else:
                    self.table[index] = current.next_node
                self.size -= 1
                return
            prev_node = current
            current = current.next_node

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.capacity = self.initial_capacity
        self.size = 0
        self.table = [None] * self.capacity

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other_dict: dict) -> None:
        for key, value in other_dict.items():
            self[key] = value

    def __iter__(self) -> None:
        for node in self.table:
            while node is not None:
                yield node.key
                node = node.next_node

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for node in self.table:
            while node is not None:
                index = hash(node.key) % new_capacity
                if new_table[index] is None:
                    new_table[index] = Node(node.key, node.value)
                else:
                    current = new_table[index]
                    while current.next_node is not None:
                        current = current.next_node
                    current.next_node = Node(node.key, node.value)
                node = node.next_node
        self.table = new_table
        self.capacity = new_capacity
