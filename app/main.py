from typing import Any


class Node:
    def __init__(
            self, key: Any,
            hash_value: int,
            value: Any,
            next_node: "Node" = None
    ) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value
        self.next_node = next_node


class Dictionary:
    def __init__(
            self, initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.table: list[Node] = [None] * initial_capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity

        # Check for collision
        current: Node = self.table[index]
        while current:
            if current.key == key and current.hash_value == hash_value:
                current.value = value
                return
            current = current.next_node

        # Add new node
        new_node: Node = Node(key, hash_value, value, self.table[index])
        self.table[index] = new_node
        self.size += 1

        # Check if resize is needed
        if self.size > self.load_factor * self.capacity:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity
        current: Node = self.table[index]

        while current:
            if current.key == key and current.hash_value == hash_value:
                return current.value
            current = current.next_node

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity: int = self.capacity * 2
        new_table: list[Node] = [None] * new_capacity

        # Rehash existing nodes into the new table
        for node in self.table:
            while node:
                new_index: int = node.hash_value % new_capacity
                new_node: Node = Node(
                    node.key, node.hash_value,
                    node.value, new_table[new_index]
                )
                new_table[new_index] = new_node
                node = node.next_node

        self.table = new_table
        self.capacity = new_capacity
