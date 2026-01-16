from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any,
                 next_node: "Node" = None) -> None:
        self.key = key
        self.value = value
        self.next_node = next_node


class Dictionary:
    def __init__(self, initial_capacity: int = 10,
                 load_factor: float = 0.75) -> None:
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
                if current.key == key:
                    current.value = value
                    return
                if current.next_node is None:
                    break
                current = current.next_node
            current.next_node = Node(key, value)
        self.size += 1
        self._check_resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._hash(key)
        current = self.table[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next_node
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _check_resize(self) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()

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
