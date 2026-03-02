from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self.capacity = initial_capacity

        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table

        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for bucket in old_table:
            if bucket:
                for node in bucket:
                    self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        h = hash(key)

        index = h % self.capacity
        if self.table[index] is None:
            self.table[index] = []
        bucket = self.table[index]
        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value, h))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        index = h % self.capacity
        bucket = self.table[index]

        if bucket is None:
            raise KeyError(f"Key not found: {key}")

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key not found: {key}")

    def __delitem__(self, key: Any) -> None:
        h = hash(key)
        index = h % self.capacity
        bucket = self.table[index]

        if bucket is None:
            raise KeyError(f"Key not found: {key}")
        for i, node in enumerate(bucket):
            if node.key == key:
                bucket.pop(i)
                self.size -= 1
                return

        raise KeyError(f"Key not found: {key}")

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0
