from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None  # Initialize the next attribute to handle chaining


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.7) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)
        node = self.table[index]

        if node is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            # Handle collision by chaining
            while node:
                if node.key == key:
                    node.value = value
                    return
                if not node.next:
                    break
                node = node.next
            node.next = Node(key, value)
            self.size += 1

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        node = self.table[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _get_index(self, key: Hashable) -> int:
        hash_value = hash(key)
        return hash_value % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for node in self.table:
            while node:
                index = hash(node.key) % new_capacity
                if new_table[index] is None:
                    new_table[index] = Node(node.key, node.value)
                else:
                    current = new_table[index]
                    while current.next:
                        current = current.next
                    current.next = Node(node.key, node.value)
                node = node.next

        self.capacity = new_capacity
        self.table = new_table
