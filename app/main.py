from typing import Any
from app.node import Node


class Dictionary:
    def __init__(self) -> None:
        self.table: list = [None] * 8
        self.capacity = len(self.table)
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        bucket = self.table[index]

        if bucket is None:
            bucket = []
            self.table[index] = bucket
        for node in bucket:
            if node.key == key:
                node.value = value
                return
        new_node = Node(key, value)
        bucket.append(new_node)
        self.size += 1

        load_factor = self.size / self.capacity
        if load_factor <= 0.75:
            return
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for bucket in self.table:
            if bucket is not None:
                for node in bucket:
                    new_index = node.hash_key % new_capacity
                    temporary_variable = new_table[new_index]
                    if temporary_variable is None:
                        temporary_variable = []
                    new_table[new_index] = temporary_variable
                    temporary_variable.append(node)

        self.table = new_table
        self.capacity = new_capacity

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        bucket = self.table[index]
        if bucket is None:
            raise KeyError("Key not found")
        for node in bucket:
            if node.key == key:
                return node.value
        raise KeyError("Key not found")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.table = [None] * 8
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity
        bucket = self.table[index]
        if bucket is None:
            raise KeyError("Key not found")

        for node in bucket:
            if node.key == key:
                bucket.remove(node)
                self.size -= 1
                return
        raise KeyError("Key not found")

    def get(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % self.capacity
        bucket = self.table[index]
        if bucket is None:
            return default
        for node in bucket:
            if node.key == key:
                return node.value
        return default

    def pop(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        bucket = self.table[index]
        if bucket is None:
            raise KeyError("Key not found")
        for node in bucket:
            if node.key == key:
                value = node.value
                bucket.remove(node)
                self.size -= 1
                return value
        raise KeyError("Key not found")

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Any:
        for bucket in self.table:
            if bucket is not None:
                for node in bucket:
                    yield node.key
