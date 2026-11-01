from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.hash_table = [None] * self.size
        self.length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.size

        while self.hash_table[index] is not None:
            node = self.hash_table[index]

            if node.hash == key_hash and (node.key is key or node.key == key):
                node.value = value
                return

            index = (index + 1) % self.size

        if (self.length + 1) / self.size > 2 / 3:
            self._resize()
            self[key] = value
            return

        self.hash_table[index] = Node(key, value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self.size

        while self.hash_table[index] is not None:
            node = self.hash_table[index]

            if node.hash == key_hash and (node.key is key or node.key == key):
                return node.value

            index = (index + 1) % self.size

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_table = self.hash_table

        self.size *= 2
        self.hash_table = [None] * self.size
        self.length = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value
