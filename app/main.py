from typing import Any


class Node:
    def __init__(self, key: Any, key_hash: int, value: Any) -> None:
        self.key = key
        self.key_hash = key_hash
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table: list[list[Node]] = [
            [] for _ in range(self.capacity)
        ]

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * 0.75:
            self._resize()

        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self.hash_table[index]

        for node in bucket:
            if node.key_hash == key_hash and node.key == key:
                node.value = value
                return

        bucket.append(Node(key, key_hash, value))
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self.hash_table[index]

        for node in bucket:
            if node.key_hash == key_hash and node.key == key:
                return node.value

        raise KeyError(f"Key {key!r} was not found")

    def __len__(self) -> int:
        return self.length

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [[] for _ in range(self.capacity)]

        for bucket in old_hash_table:
            for node in bucket:
                index = self._get_index(node.key_hash)
                self.hash_table[index].append(node)
