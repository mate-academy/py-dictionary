from typing import Union


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 2 / 3
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [None] * self.capacity

    class Node:
        def __init__(
                self,
                key: Union[str, int, float],
                value: Union[str, int, float]
        ) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)

    def _hash_index(self, key: Union[str, int, float]) -> int:
        return hash(key) % self.capacity

    def __setitem__(
            self, key: Union[str, int, float],
            value: Union[str, int, float]
    ) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index = self._hash_index(key)

        while self.buckets[index] is not None:
            if self.buckets[index].key == key:
                self.buckets[index].value = value
                return
            index = (index + 1) % self.capacity

        self.buckets[index] = self.Node(key, value)
        self.size += 1

    def __getitem__(
            self,
            key: Union[str, int, float]
    ) -> Union[str, int, float]:
        index = self._hash_index(key)

        while self.buckets[index] is not None:
            if self.buckets[index].key == key:
                return self.buckets[index].value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0  # Перезапис розміру

        for node in old_buckets:
            if node is not None:
                self[node.key] = node.value
