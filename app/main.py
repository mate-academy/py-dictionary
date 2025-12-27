from dataclasses import dataclass
from typing import Hashable, Iterator


@dataclass
class Node:
    key: Hashable
    value: any
    hash_value: int


class Dictionary:
    INITIAL_CAPACITY = 8
    THRESHOLD = 2 / 3.0
    CAPACITY_MULTIPLIER = 2

    def __init__(self, initial_capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * self.CAPACITY_MULTIPLIER
        new_buckets = [[] for _ in range(new_capacity)]

        for bucket in self.buckets:
            for node in bucket:
                new_index = node.hash_value % new_capacity
                new_buckets[new_index].append(node)

        self.capacity = new_capacity
        self.buckets = new_buckets

    def __setitem__(self, key: Hashable, value: any) -> None:
        hash_key = hash(key)
        index = self._get_index(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        new_node = Node(key=key, value=value, hash_value=hash_key)
        bucket.append(new_node)
        self.size += 1

        load_factor = self.size / self.capacity
        if load_factor > self.THRESHOLD:
            self._resize()

    def __getitem__(self, key: Hashable) -> any:
        index = self._get_index(key)
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Key {key} not found in dictionary.")

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        bucket = self.buckets[index]

        for i, node in enumerate(bucket):
            if node.key == key:
                del bucket[i]
                self.size -= 1
                return

        raise KeyError(f"Key {key} not found in dictionary.")

    def clear(self) -> None:
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    def __iter__(self) -> Iterator[Hashable]:
        for bucket in self.buckets:
            for node in bucket:
                yield node.key
