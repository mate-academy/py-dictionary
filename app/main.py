from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        if not self.table[index]:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            node = self.table[index]
            while node.next:
                if node.key == key:
                    node.value = value
                    return
                node = node.next
            if node.key == key:
                node.value = value
            else:
                node.next = Node(key, value)
                self.size += 1

    def __getitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        node = self.table[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(key)

    def __len__(self) -> None:
        return self.size
