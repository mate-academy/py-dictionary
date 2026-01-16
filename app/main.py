from typing import Any, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        self.key = key
        self.value = value
        self.key_hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.load_factor = 0
        self.capacity = 8
        self.buckets = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.load_factor >= self.capacity * 2 / 3:
            self._resize(self.buckets)

        index = self.get_index(key)
        while self.buckets[index] and self.buckets[index].key != key:
            index = (index + 1) % self.capacity

        if not self.buckets[index]:
            self.load_factor += 1
        self.buckets[index] = Node(key, value)

    def __getitem__(self, input_key: Any) -> Any:
        index = self.get_index(input_key)

        while self.buckets[index] is not None:
            node = self.buckets[index]
            if node.key == input_key:
                return node.value
            index = (index + 1) % self.capacity

        raise KeyError("Wrong key")

    def _resize(self, elements: list) -> None:
        self.capacity *= 2
        self.buckets = [None] * self.capacity

        for node in elements:
            if node is not None:
                index = node.key_hash % self.capacity

                while self.buckets[index] is not None:
                    index = (index + 1) % self.capacity

                self.buckets[index] = node

    def get_index(self, input_key: Any) -> Any:
        hash_key = hash(input_key)
        return hash_key % self.capacity

    def __len__(self) -> int:
        return self.load_factor
