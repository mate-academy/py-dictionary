from typing import Any


class Node:
    def __init__(
        self,
        key: Any,
        hash_value: int,
        value: Any,
    ) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 0.75

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.table: list[list[Node]] = [
            [] for _ in range(self.capacity)
        ]

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = hash(key)
        bucket_index = hash_value % self.capacity
        bucket = self.table[bucket_index]

        for node in bucket:
            if node.hash == hash_value and node.key == key:
                node.value = value
                return

        bucket.append(Node(key, hash_value, value))
        self.size += 1

        if self.size / self.capacity > self.LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        bucket_index = hash_value % self.capacity
        bucket = self.table[bucket_index]

        for node in bucket:
            if node.hash == hash_value and node.key == key:
                return node.value

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        hash_value = hash(key)
        bucket_index = hash_value % self.capacity
        bucket = self.table[bucket_index]

        for node_index, node in enumerate(bucket):
            if node.hash == hash_value and node.key == key:
                del bucket[node_index]
                self.size -= 1
                return

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]

        for bucket in old_table:
            for node in bucket:
                bucket_index = node.hash % self.capacity
                self.table[bucket_index].append(node)
