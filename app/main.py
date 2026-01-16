from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value
        self.next = None


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            while node:
                self[node.key] = node.value
                node = node.next

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self.__resize()

        key_hash = hash(key)
        index = key_hash % self.capacity

        node = self.table[index]

        if node is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            while node:
                if node.key == key:
                    node.value = value
                    return
                if node.next is None:
                    break
                node = node.next
            node.next = Node(key, value)
            self.size += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        node = self.table[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key {key} is not found.")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        for node in self.table:
            if node.next is None:
                continue
            while node:
                node.next, node = None, node.next
        self.table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity

        node = self.table[index]
        prev_node = None

        while node:
            if node.key == key:
                if prev_node is None:
                    self.table[index] = node.next
                else:
                    prev_node.next = node.next
                self.size -= 1
                return
            prev_node = node
            node = node.next

        raise KeyError(f"Key {key} is not found.")

    def get(self, key: Any, default: Any = None) -> None:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"Key {key} is not found.")

    def update(self, other: Any = None, **kwargs) -> None:
        if other:
            if isinstance(other, Dictionary):
                for key in other:
                    self[key] = other[key]
            else:
                for key, value in other.items():
                    self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def __iter__(self) -> Any:
        for node in self.table:
            while node:
                yield node.key
                node = node.next
