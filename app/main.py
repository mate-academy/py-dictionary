from typing import Any, Hashable, List


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table: List[List[Node]] = [[] for _ in range(self.capacity)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [[] for _ in range(self.capacity)]
        self.length = 0

        for bucket in old_hash_table:
            for node in bucket:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length / self.capacity >= 0.7:
            self._resize()

        index = self._hash(key)

        for node in self.hash_table[index]:
            if node.key == key:
                node.value = value
                return

        self.hash_table[index].append(Node(key, value))
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)
        for node in self.hash_table[index]:
            if node.key == key:
                return node.value
        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.length
