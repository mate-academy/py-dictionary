from typing import Hashable, Any


class Node:
    def __init__(
            self,
            key: Hashable,
            hash_value: int,
            value: Any
    ) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value
        self.next = None


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 16,
            load_factor: float = 0.67
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        if self.size >= self.capacity * self.load_factor:
            self._resize()

        current = self.table[index]
        prev = None

        while current:
            if current.key == key and current.hash_value == hash_value:
                current.value = value
                return
            prev, current = current, current.next

        new_node = Node(key, hash_value, value)
        if prev:
            prev.next = new_node
        else:
            self.table[index] = new_node

        self.size += 1

    def __getitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity
        current = self.table[index]

        while current:
            if current.key == key and current.hash_value == hash_value:
                return current.value
            current = current.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for i in range(self.capacity):
            current = self.table[i]
            while current:
                new_index = current.hash_value % new_capacity
                new_node = Node(current.key, current.hash_value, current.value)
                if new_table[new_index] is None:
                    new_table[new_index] = new_node
                else:
                    new_node.next = new_table[new_index]
                    new_table[new_index] = new_node
                current = current.next

        self.table = new_table
        self.capacity = new_capacity
