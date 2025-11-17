from __future__ import annotations
from typing import Iterator, Any


class Node:
    def __init__(self, key: Any, value: Any, key_hash: int) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash: int = key_hash


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 10
        self.threshold: int = self.capacity // 2
        self.nodes: list[Node | list[Node] | None] = [None] * self.capacity
        self.size: int = 0
        self._keys: list[Any] = []

    def resize(self) -> None:
        old_nodes: list[Node | list[Node] | None] = self.nodes
        self.capacity *= 2
        self.threshold = self.capacity // 2
        self.nodes = [None] * self.capacity
        self.size = 0

        for slot in old_nodes:
            if slot is None:
                continue
            if isinstance(slot, Node):
                self[slot.key] = slot.value
                continue
            for node in slot:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size >= self.threshold:
            self.resize()
        _hash: int = hash(key)
        _index: int = _hash % self.capacity
        slot = self.nodes[_index]

        if slot is None:
            self.nodes[_index] = Node(key, value, _hash)
            self.size += 1
            self._keys.append(key)
            return

        if isinstance(slot, Node):
            if slot.key == key:
                slot.value = value
                return
            self.nodes[_index] = [slot, Node(key, value, _hash)]
            self.size += 1
            self._keys.append(key)
            return

        for node in slot:
            if node.key == key:
                node.value = value
                return

        slot.append(Node(key, value, _hash))
        self._keys.append(key)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        _index: int = hash(key) % self.capacity
        slot = self.nodes[_index]

        if slot is None:
            raise KeyError(key)

        if isinstance(slot, Node):
            if slot.key == key:
                return slot.value
            raise KeyError(key)

        for node in slot:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.capacity = 10
        self.threshold = self.capacity // 2
        self.nodes = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        _index: int = hash(key) % self.capacity
        slot = self.nodes[_index]

        if slot is None:
            raise KeyError(key)

        if isinstance(slot, Node):
            if slot.key == key:
                self.nodes[_index] = None
                self.size -= 1
                return
            raise KeyError(key)

        for i, node in enumerate(slot):
            if node.key == key:
                slot.pop(i)
                self.size -= 1
                if len(slot) == 1:
                    self.nodes[_index] = slot[0]
                elif len(slot) == 0:
                    self.nodes[_index] = None
                return

        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise

    def items(self) -> Iterator[tuple[Any, Any]]:
        for slot in self.nodes:
            if slot is None:
                continue
            if isinstance(slot, Node):
                yield (slot.key, slot.value)
            else:
                for node in slot:
                    yield (node.key, node.value)

    def update(self, other: list | dict | Dictionary) -> None:
        if hasattr(other, "items"):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for key in self._keys:
            yield key
