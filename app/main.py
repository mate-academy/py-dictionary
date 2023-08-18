from typing import Any, Hashable


class Default:
    pass


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self, new_capacity: int) -> None:
        old_table = self.table
        self.table = [None] * new_capacity
        self.capacity = new_capacity
        self.size = 0
        for node in old_table:
            while node:
                self[node.key] = node.value
                node = node.next

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._hash(key)
        new_node = Node(key, value)
        if self.table[index] is None:
            self.table[index] = new_node
        else:
            current = self.table[index]
            while current:
                if current.key == key and hash(current.key) == hash(key):
                    current.value = value  # Replace existing value
                    return
                current = current.next
            new_node.next = self.table[index]
            self.table[index] = new_node
        self.size += 1
        if self.size / self.capacity >= self.load_factor:
            self._resize(self.capacity * 2)

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key and hash(current.key) == hash(key):
                return current.value
            current = current.next
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Any) -> None:
        index = self._hash(key)
        current = self.table[index]
        prev = None
        while current:
            if current.key == key and hash(current.key) == hash(key):
                if prev is None:
                    self.table[index] = current.next
                else:
                    prev.next = current.next
                self.size -= 1
                return
            prev = current
            current = current.next
        raise KeyError(key)

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = Default) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is Default:
                raise
            return default

    def update(self, other_dict: dict) -> None:
        for key, value in other_dict.items():
            self[key] = value

    def __iter__(self) -> Any:
        for node in self.table:
            while node:
                yield node.key
                node = node.next


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.next = None
