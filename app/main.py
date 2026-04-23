from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.value = value
        self.key = key
        self.hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.storage = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        if self.storage[index] is None:
            self.storage[index] = [Node(key, value)]
            self.size += 1
            return

        for node in self.storage[index]:
            if node.hash == key_hash and node.key == key:
                node.value = value
                return

        self.storage[index].append(Node(key, value))
        self.size += 1
        if self.size / self.capacity > 0.75:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        bucket = self.storage[index]
        if bucket is not None:
            for node in bucket:
                if node.hash == key_hash and node.key == key:
                    return node.value

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        old_storage = self.storage
        self.capacity *= 2
        self.storage = [None] * self.capacity
        self.size = 0

        for bucket in old_storage:
            if bucket is not None:
                for node in bucket:
                    self.__setitem__(node.key, node.value)
