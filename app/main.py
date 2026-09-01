from typing import Any


class Node:
    def __init__(self, key: Any, hash_code: int, value: Any) -> None:
        self.key = key
        self.hash_code = hash_code
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8

    def _capacity(self) -> int:
        return len(self.hash_table)

    def _find_index(self, key: Any, hash_code: int) -> int:
        index = hash_code % self._capacity()
        while True:
            node = self.hash_table[index]
            if node is None or (
                node.hash_code == hash_code and node.key == key
            ):
                return index
            index = (index + 1) % self._capacity()

    def _resize(self) -> None:
        old_table = self.hash_table
        self.hash_table = [None] * (self._capacity() * 2)
        self.length = 0
        for node in old_table:
            if node is not None:
                self._insert(node)

    def _insert(self, node: Node) -> None:
        index = self._find_index(node.key, node.hash_code)
        if self.hash_table[index] is None:
            self.length += 1
        self.hash_table[index] = node

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length / self._capacity() >= 2 / 3:
            self._resize()
        self._insert(Node(key, hash(key), value))

    def __getitem__(self, key: Any) -> Any:
        hash_code = hash(key)
        node = self.hash_table[self._find_index(key, hash_code)]
        if node is None:
            raise KeyError(f"Key {key} does not exist")
        return node.value

    def __len__(self) -> int:
        return self.length
