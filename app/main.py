from dataclasses import dataclass
from typing import Hashable


@dataclass
class Node:
    key: Hashable
    value: any
    hash_value: int


class Dictionary:
    initial_capacity = 8
    threshold = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets = [[] for _ in range(new_capacity)]

        for bucket in self.buckets:
            for node in bucket:
                new_idx = node.hash_value % new_capacity
                new_buckets[new_idx].append(node)

        self.capacity = new_capacity
        self.buckets = new_buckets

    def __setitem__(self, key: Hashable, value: any) -> None:
        idx = self._get_index(key)
        hash_value = hash(key)

        for node in self.buckets[idx]:
            if node.key == key:
                node.value = value
                return

        new_node = Node(key=key, value=value, hash_value=hash_value)
        self.buckets[idx].append(new_node)
        self.size += 1

        if self.size / self.capacity > self.threshold:
            self._resize()

    def __getitem__(self, key: Hashable) -> any:
        idx = self._get_index(key)
        for node in self.buckets[idx]:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size
