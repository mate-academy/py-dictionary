from dataclasses import dataclass


@dataclass
class Node:
    key: object
    hash_value: int
    value: object


class Dictionary:
    def __init__(self, initial_capacity: int = 8, load_factor: float = 0.7, ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    def _index_for_hash(self, hash_value: int) -> int:
        return hash_value % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets = [[] for _ in range(new_capacity)]

        for bucket in self.buckets:
            for node in bucket:
                new_index = node.hash_value % new_capacity
                new_buckets[new_index].append(node)

        self.buckets = new_buckets
        self.capacity = new_capacity

    def __setitem__(self, key, value):
        hash_value = hash(key)
        index = hash_value % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return
        bucket.append(Node(key, hash_value, value))
        self.size += 1

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity
        bucket = self.buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size








