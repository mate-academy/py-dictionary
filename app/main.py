from dataclasses import dataclass
from typing import Any

_DELETED = object()


@dataclass
class Node:
    node_key: Any
    node_hash: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.slots: list[Node] = [None] * 8
        self.length: int = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._find_slot(key)
        if self.slots[index] is None:
            self.slots[index] = Node(key, hash(key), value)
            self.length += 1

            if self.length > len(self.slots) * 2 / 3:
                self._resize()
        else:
            self.slots[index].value = value

    def __getitem__(self, key: Any) -> Any:
        index = self._find_slot(key)
        if self.slots[index] is None or self.slots[index] is _DELETED:
            raise KeyError(f"Key not found: {key}")
        return self.slots[index].value

    def __len__(self) -> int:
        return self.length

    def _find_slot(self, key: Any) -> int:
        key_hash = hash(key)
        index = key_hash % len(self.slots)
        first_deleted_idx = None
        while True:
            node = self.slots[index]

            if node is None:
                return (
                    first_deleted_idx
                    if first_deleted_idx is not None
                    else index
                )

            if node is _DELETED:
                if first_deleted_idx is None:
                    first_deleted_idx = index
            elif node.node_hash == key_hash and node.node_key == key:
                return index

            index = (index + 1) % len(self.slots)

    def _resize(self) -> None:
        old_slots = self.slots

        new_size = len(old_slots) * 2
        self.slots = [None] * new_size

        self.length = 0
        for node in old_slots:
            if node is not None and node is not _DELETED:
                self.__setitem__(node.node_key, node.value)

    def __delitem__(self, key: Any) -> None:
        index = self._find_slot(key)
        if self.slots[index] is None or self.slots[index] is _DELETED:
            raise KeyError(f"Key not found: {key}")

        self.slots[index] = _DELETED
        self.length -= 1

    def clear(self) -> None:
        self.slots = [None] * 8
        self.length = 0
