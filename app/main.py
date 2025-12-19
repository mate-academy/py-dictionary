from typing import Any, Hashable
from collections.abc import Iterable, Mapping


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.key_hash = hash(key)
        self.value = value


class Dictionary:
    _MISSING = object()
    _DELETED = object()

    def __init__(self) -> None:
        self.size = 0
        self.CAPACITY = 8
        self.node_list = [None] * self.CAPACITY

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= int(self.CAPACITY * 2 / 3):
            self._resize()
        h = hash(key)
        index = h % self.CAPACITY
        while True:
            node = self.node_list[index]
            if node is None or node == self._DELETED:
                self.node_list[index] = Node(key, value)
                self.size += 1
                break
            elif node.key_hash == h and node.key == key:
                node.value = value
                break
            index = (index + 1) % self.CAPACITY

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.CAPACITY
        h = hash(key)
        start_index = index
        while self.node_list[index] is not None:
            node = self.node_list[index]
            if (node != self._DELETED
                    and h == node.key_hash and node.key == key):
                return node.value
            index = (index + 1) % self.CAPACITY
            if index == start_index:
                break
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.CAPACITY
        start_index = index
        h = hash(key)
        while self.node_list[index] is not None:
            node = self.node_list[index]
            if node is not None and node != self._DELETED:
                if node.key_hash == h and node.key == key:
                    self.node_list[index] = self._DELETED
                    self.size -= 1
                    return
            index = (index + 1) % self.CAPACITY
            if index == start_index:
                break
        raise KeyError(f"Key {key} not found")

    def __iter__(self) -> Hashable:
        for node in self.node_list:
            if node is not None and node != self._DELETED:
                yield node.key

    def items(self) -> Any:
        for node in self.node_list:
            if node is not None and node != self._DELETED:
                yield node.key, node.value

    def values(self) -> Any:
        for node in self.node_list:
            if node is not None and node != self._DELETED:
                yield node.value

    def _resize(self) -> None:
        old_node = [node for node in self.node_list
                    if node is not None and node is not self._DELETED]
        self.CAPACITY *= 2
        self.node_list = [None] * self.CAPACITY
        self.size = 0
        for node in old_node:
            self[node.key] = node.value

    def get(self, key: Hashable, default: Any = None) -> Any:
        index = hash(key) % self.CAPACITY
        h = hash(key)
        start_index = index

        while self.node_list[index] is not None:
            node = self.node_list[index]
            if (node != self._DELETED
                    and h == node.key_hash
                    and node.key == key):
                return node.value
            index = (index + 1) % self.CAPACITY
            if index == start_index:
                break
        return default

    def clear(self) -> None:
        self.node_list = [None] * self.CAPACITY
        self.size = 0

    def pop(self, key: Hashable, default: Any = _MISSING) -> Any:
        index = hash(key) % self.CAPACITY
        start_index = index
        h = hash(key)
        while self.node_list[index] is not None:
            node = self.node_list[index]
            if node is not None and node != self._DELETED:
                if node.key_hash == h and node.key == key:
                    value = node.value
                    self.node_list[index] = self._DELETED
                    self.size -= 1
                    return value
            index = (index + 1) % self.CAPACITY
            if index == start_index:
                break
        if default is not self._MISSING:
            return default
        raise KeyError(f"Key {key} not found")

    def update(self, other: Any = None, **kwargs: Any) -> None:
        if other is not None:
            if isinstance(other, Mapping):
                for key, value in other.items():
                    self[key] = value
                return
            elif isinstance(other, Iterable):
                for key, value in other:
                    self[key] = value
                return
            raise TypeError("update() argument must be"
                            " a mapping or iterable of key/value pairs")
        for key, value in kwargs.items():
            self[key] = value
