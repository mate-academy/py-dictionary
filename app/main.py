from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value
        self.next = None


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = load_factor
        self.buckets = [None] * self.capacity

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._hash(key)
        hash_value = hash(key)

        node = self.buckets[index]

        while node:
            if node.hash == hash_value and node.key == key:
                node.value = value
                return
            node = node.next

        new_node = Node(key, value, hash_value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)
        hash_value = hash(key)
        node = self.buckets[index]

        while node:
            if node.hash == hash_value and node.key == key:
                return node.value
            node = node.next

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0

        for bucket in old_buckets:
            node = bucket
            while node:
                self[node.key] = node.value
                node = node.next

    def __delitem__(self, key: Any) -> None:
        index = self._hash(key)
        hash_value = hash(key)
        prev = None
        node = self.buckets[index]

        while node:
            if node.hash == hash_value and node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[index] = node.next
                self.size -= 1
                return
            prev, node = node, node.next

        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self) -> Any:
        for bucket in self.buckets:
            node = bucket
            while node:
                yield node.key
                node = node.next

    def items(self) -> Any:
        for bucket in self.buckets:
            node = bucket
            while node:
                yield node.key, node.value
                node = node.next

    def keys(self) -> Any:
        return iter(self)

    def values(self) -> Any:
        for _, value in self.items():
            yield value
