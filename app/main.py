import dataclasses
from typing import Any


@dataclasses.dataclass
class Node:
    key: Any
    value: Any
    hash_key: int


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.buckets = [None] * self.capacity
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        if (self.size + 1) / self.capacity > (2 / 3):
            self.resize()
        index = hash_key % self.capacity
        bucket = self.buckets[index]
        if bucket is None:
            self.buckets[index] = [Node(key, value, hash_key)]
            self.size += 1
            return
        for node in bucket:
            if node.key == key:
                node.value = value
                return
        bucket.append(Node(key, value, hash_key))
        self.size += 1

    def __getitem__(self, item: Any) -> Any:
        hash_item = hash(item)
        index = hash_item % self.capacity
        bucket = self.buckets[index]
        if bucket is None:
            raise KeyError(item)
        for node in bucket:
            if node.key == item:
                return node.value
        raise KeyError(item)

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        for bucket in old_buckets:
            if bucket is not None:
                for node in bucket:
                    new_index = node.hash_key % self.capacity
                    if self.buckets[new_index] is None:
                        self.buckets[new_index] = []
                    self.buckets[new_index].append(node)
                    self.size += 1
