from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity: int = capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.table = [None] * self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)
        if self.table[index] is None:
            self.table[index] = Node(key, value)
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = Node(key, value)
        self.size += 1
        if self.size > self.capacity * self.load_factor:
            self.resize()

    def __len__(self) -> int:
        return self.size

    def get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for node in self.table:
            while node:
                self.__setitem__(node.key, node.value)
                node = node.next
        self.capacity = new_capacity
        self.table = new_table
