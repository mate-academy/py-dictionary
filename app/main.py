from typing import Any


class Node:
    def __init__(self, key: Any, hash_: int, value: Any) -> None:
        self.key = key
        self.hash = hash_
        self.value = value


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 0.75

    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * self.INITIAL_CAPACITY

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.length + 1) / len(self.hash_table) > self.LOAD_FACTOR:
            self._resize()

        key_hash = hash(key)
        index = key_hash % len(self.hash_table)

        while self.hash_table[index] is not None:
            node = self.hash_table[index]

            if node.hash == key_hash and node.key == key:
                node.value = value
                return

            index = (index + 1) % len(self.hash_table)

        self.hash_table[index] = Node(key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % len(self.hash_table)
        start_index = index

        while self.hash_table[index] is not None:
            node = self.hash_table[index]

            if node.hash == key_hash and node.key == key:
                return node.value

            index = (index + 1) % len(self.hash_table)

            if index == start_index:
                break

        raise KeyError(f"Key {key!r} not found")

    def _resize(self) -> None:
        old_hash_table = self.hash_table

        self.hash_table = [None] * (len(old_hash_table) * 2)
        self.length = 0

        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value
