from dataclasses import dataclass
from typing import Any, Hashable, Iterator


@dataclass
class Node:
    key: Hashable
    value: Any
    _hash: int


class Dictionary:
    _MISSING = object()
    _load_factor = 2 / 3

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
        if (self.length + 1) / self.hash_table_size >= Dictionary._load_factor:
            self._resize()
        key_hash = hash(key)
        key_index = self.index_found(key)
        for node in self.hash_table[key_index]:
            if node._hash == key_hash and node.key == key:
                node.value = value
                return
        self.hash_table[key_index].append(
            Node(
                key=key,
                value=value,
                _hash=key_hash
            )
        )
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        key_index = self.index_found(key)
        for node in self.hash_table[key_index]:
            if node._hash == key_hash:
                if node.key == key:
                    return node.value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.length = 0
        self.hash_table_size = 8
        self.hash_table = [[] for _ in range(self.hash_table_size)]

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        key_index = self.index_found(key)
        for index, node in enumerate(self.hash_table[key_index]):
            if node._hash == key_hash:
                if node.key == key:
                    del self.hash_table[key_index][index]
                    self.length -= 1
                    return
        raise KeyError(key)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = _MISSING) -> Any:
        try:
            temp = self[key]
            del self[key]
            return temp
        except KeyError:
            if default is Dictionary._MISSING:
                raise KeyError(key)
            else:
                return default

    def update(self, *args, **kwargs) -> None:
        if len(args) > 1:
            raise TypeError("update expected at most 1 argument, got 2")
        if args:
            to_update = args[0]
            if hasattr(to_update, "keys"):
                for key in to_update.keys():
                    self[key] = to_update[key]
            else:
                for key, value in to_update:
                    self[key] = value

        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def __iter__(self) -> Iterator[Hashable]:
        for bucket in self.hash_table:
            for node in bucket:
                yield node.key
