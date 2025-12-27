from typing import Any, Hashable


class Node:
    def __init__(
            self, key: Hashable,
            value: Any,
            hash_value: float
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value
        self.next = None


class Dictionary:
    def __init__(
            self, initial_capacity: float = 16,
            load_factor: float = 0.75
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def _hash_function(self, key: Hashable) -> float:
        return hash(key) % self.capacity

    def _resize(self, new_capacity: Any) -> None:
        old_table = self.table
        self.table = [None] * new_capacity
        self.capacity = new_capacity
        self.size = 0

        for node in old_table:
            while node:
                self[node.key] = node.value
                node = node.next

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = self._hash_function(key)
        if hash_value < 0 or hash_value >= self.capacity:
            raise ValueError("Некоректне значення хешу")

        new_node = Node(key, value, hash_value)
        # Зберегти значення хешу в об'єкті Node

        if self.table[hash_value] is None:
            self.table[hash_value] = new_node
        else:
            current_node = self.table[hash_value]
            while current_node:
                if current_node.hash == hash_value and current_node.key == key:
                    current_node.value = value
                    return
                current_node = current_node.next

            new_node.next = self.table[hash_value]
            self.table[hash_value] = new_node

        self.size += 1
        if self.size / self.capacity >= self.load_factor:
            self._resize(self.capacity * 2)

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = self._hash_function(key)
        if hash_value < 0 or hash_value >= self.capacity:
            raise ValueError("Некоректне значення хешу")

        current_node = self.table[hash_value]

        while current_node:
            if current_node.hash == hash_value and current_node.key == key:
                return current_node.value
            current_node = current_node.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
