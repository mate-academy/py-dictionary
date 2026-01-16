from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, key_hash: int, value: Any) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self.capacity = initial_capacity
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        self.load_factor = load_factor

    def _index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def _should_resize(self) -> bool:
        return (self.size + 1) / self.capacity > self.load_factor

    def _resize(self, new_capacity: int) -> None:
        self.capacity = new_capacity
        new_buckets = [[] for _ in range(self.capacity)]
        for nodes in self.buckets:
            for node in nodes:
                node_index = self._index(node.hash)
                new_buckets[node_index].append(node)
        self.buckets = new_buckets

    def _find_node(self, bucket: list[Node], key: Hashable,
                   key_hash: int) -> tuple | None:
        for index, node in enumerate(bucket):
            if node.hash == key_hash and node.key == key:
                return (index, node)
        return None

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        bucket_index = self._index(key_hash)
        bucket = self.buckets[bucket_index]
        found = self._find_node(bucket, key, key_hash)
        if found is not None:
            node_index, node = found
            node.value = value
            return
        if self._should_resize():
            self._resize(self.capacity * 2)
            bucket_index = self._index(key_hash)
            bucket = self.buckets[bucket_index]
            bucket.append(Node(key, key_hash, value))
            self.size += 1
        else:
            bucket.append(Node(key, key_hash, value))
            self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        bucket_index = self._index(key_hash)
        bucket = self.buckets[bucket_index]
        found = self._find_node(bucket, key, key_hash)
        if found is not None:
            _, node = found
            return node.value
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.size
