from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        if not self.table[index]:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if not current.next:
                    break
                current = current.next
            current.next = Node(key, value)
            self.size += 1
        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity
        for node in self.table:
            while node:
                index = hash(node.key) % self.capacity
                if not new_table[index]:
                    new_table[index] = Node(node.key, node.value)
                else:
                    current = new_table[index]
                    while current.next:
                        current = current.next
                    current.next = Node(node.key, node.value)
                node = node.next
        self.table = new_table
