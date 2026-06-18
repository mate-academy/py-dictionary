from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, h: int) -> None:
        self.key = key
        self.value = value
        self.hash = h  # O hash é armazenado na criação e nunca recalculado


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size: int = 0
        self.table: list[list[Node]] = [[] for _ in range(self.capacity)]

    def _get_index(self, h: int) -> int:
        return h % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for node in bucket:
                index = self._get_index(node.hash)
                self.table[index].append(node)
                self.size += 1

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        h = hash(key)
        index = self._get_index(h)
        bucket = self.table[index]

        for node in bucket:
            if node.hash == h and node.key == key:
                node.value = value
                return

        bucket.append(Node(key, value, h))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        index = self._get_index(h)
        for node in self.table[index]:
            if node.hash == h and node.key == key:
                return node.value
        raise KeyError(f"Key '{key}' not found.")

    def __delitem__(self, key: Any) -> None:
        h = hash(key)
        index = self._get_index(h)
        bucket = self.table[index]
        for i, node in enumerate(bucket):
            if node.hash == h and node.key == key:
                del bucket[i]
                self.size -= 1
                return
        raise KeyError(f"Key '{key}' not found.")

    def __len__(self) -> int:
        return self.size
