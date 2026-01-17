from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash_value = hash_value
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __hash_function(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for node in self.table:
            while node:
                new_index = hash(node.key) % new_capacity
                new_node = Node(node.key, node.value, node.hash_value)
                new_node.next = new_table[new_index]
                new_table[new_index] = new_node
                node = node.next

        self.table = new_table
        self.capacity = new_capacity
        print(f"Resized dictionary to new capacity: {new_capacity}")

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self.__hash_function(key)
        current_node = self.table[index]

        while current_node:
            if current_node.key == key:
                current_node.value = value
                return
            current_node = current_node.next

        new_node = Node(key, value, hash(key))
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self.__resize()

    def __getitem__(self, key: Any) -> Any:
        index = self.__hash_function(key)
        current_node = self.table[index]

        while current_node:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next

        raise KeyError(f"Key '{key}' not in dictionary")

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        items = []
        for node in self.table:
            while node:
                items.append(f"{node.key}: {node.value}")
                node = node.next
        return "{" + ", ".join(items) + "}"
