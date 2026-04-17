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
        index = hash_key % self.capacity
        bucket = self.buckets[index]
        if bucket is None:
            bucket_buckets = []
            node = Node(key, value, hash_key)
            bucket_buckets.append(node)
            self.buckets[index] = bucket_buckets
            self.size += 1
            return
        for node in bucket:
            if node.key == key:
                node.value = value
                return
        node = Node(key, value, hash_key)
        bucket.append(node)
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
