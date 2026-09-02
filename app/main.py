from dataclasses import dataclass
from typing import Any, Hashable, Iterator

_SENTINEL = object()


@dataclass
class Node:
    key: Hashable
    hash: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list[list[Node]] = [[] for _ in range(8)]
        self.max_load_factor = 0.75

    def get_index(self, key_hash: int) -> int:
        return key_hash % len(self.hash_table)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self.get_index(key_hash)

        for node in self.hash_table[index]:
            if node.key == key:
                node.value = value
                return

        self.hash_table[index].append(Node(key=key, hash=key_hash, value=value))
        self.length += 1

        if self.length / len(self.hash_table) >= self.max_load_factor:
            self.resize()

    def resize(self) -> None:
        old_table = self.hash_table
        self.hash_table = [[] for _ in range(len(old_table) * 2)]
        self.length = 0

        for bucket in old_table:
            for node in bucket:
                self[node.key] = node.value

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = self.get_index(key_hash)
        for node in self.hash_table[index]:
            if node.key == key:
                return node.value
        raise KeyError(f"Key '{key}' not found")

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(8)]
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = self.get_index(key_hash)
        for i, node in enumerate(self.hash_table[index]):
            if node.key == key:
                self.hash_table[index].pop(i)
                self.length -= 1
                return
        raise KeyError(f"Key '{key}' not found")

    def pop(self, key: Hashable, default: Any = _SENTINEL) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not _SENTINEL:
                return default
            raise KeyError(f"Key '{key}' not found")

    def update(self, other: Any) -> None:
        if hasattr(other, "items"):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for bucket in self.hash_table:
            for node in bucket:
                yield node.key