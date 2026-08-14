from typing import Any


class Node:
    def __init__(self, key: Any, key_hash: int, value: Any) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor = 0.7
        self.table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self.table[index]

        for node in bucket:
            if node.hash == key_hash and node.key == key:
                node.value = value
                return

        bucket.append(Node(key, key_hash, value))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._get_index(key_hash)
        bucket = self.table[index]

        for node in bucket:
            if node.hash == key_hash and node.key == key:
                return node.value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def _resize(self) -> None:
        old_table = self.table

        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]

        for bucket in old_table:
            for node in bucket:
                index = self._get_index(node.hash)
                self.table[index].append(node)
