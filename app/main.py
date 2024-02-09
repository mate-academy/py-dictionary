from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None


class Dictionary:
    def __init__(self, capacity: int = 11, load_factor: float = 0.5) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index: int = hash(key) % self.capacity
        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current.next:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            if current.key == key:
                current.value = value
            else:
                current.next = Node(key, value)
                self.size += 1
        if self.size > self.capacity * self.load_factor:
            self.resize()

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

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for i in range(self.capacity):
            current = self.table[i]
            while current:
                new_index = hash(current.key) % new_capacity
                if new_table[new_index] is None:
                    new_table[new_index] = Node(current.key, current.value)
                else:
                    new_current = new_table[new_index]
                    while new_current.next:
                        new_current = new_current.next
                    new_current.next = Node(current.key, current.value)
                current = current.next
        self.table = new_table
        self.capacity = new_capacity

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        current = self.table[index]
        if current is None:
            raise KeyError(key)
        if current.key == key:
            self.table[index] = current.next
            self.size -= 1
            return
        previous = current
        current = current.next
        while current:
            if current.key == key:
                previous.next = current.next
                self.size -= 1
                return
            previous = current
            current = current.next
        raise KeyError(key)

    def get(self, key: Hashable) -> Any:
        try:
            return self[key]
        except KeyError:
            return "The key does not exist"

    def pop(self, key: Hashable) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return "The key does not exist"

    def update(self, other: list) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> None:
        for node in self.table:
            while node:
                yield node.key
                node = node.next
