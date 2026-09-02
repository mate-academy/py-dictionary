from dataclasses import dataclass
from typing import Any, Hashable


@dataclass
class Node:
    key: Hashable
    value: Any
    _hash: int


class Dictionary:
    load_factor = 2 / 3

    def __init__(self, hash_table_size: int = 8) -> None:
        self.hash_table_size = hash_table_size
        self.hash_table = [[] for _ in range(hash_table_size)]
        self.length = 0

    def index_found(self, key: Hashable) -> int:
        return hash(key) % self.hash_table_size

    def _resize(self) -> None:
        self.hash_table_size *= 2
        self.new_hash_table = [[] for _ in range(self.hash_table_size)]
        for bucket in self.hash_table:
            for node in bucket:
                key_index = node._hash % self.hash_table_size
                self.new_hash_table[key_index].append(node)
        self.hash_table = self.new_hash_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if (self.length + 1) / self.hash_table_size >= Dictionary.load_factor:
            self._resize()
        key_index = self.index_found(key)
        for node in self.hash_table[key_index]:
            if node._hash != hash(key):
                continue
            if node.key == key:
                node.value = value
                return
        self.hash_table[key_index].append(
            Node(
                key=key,
                value=value,
                _hash=hash(key)
            )
        )
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_index = self.index_found(key)
        for node in self.hash_table[key_index]:
            if node._hash == hash(key):
                if node.key == key:
                    return node.value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.length = 0
        self.hash_table_size = 8
        self.hash_table = [[] for _ in range(self.hash_table_size)]
