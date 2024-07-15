from typing import Any, Optional, Iterator, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        self.key: Hashable = key
        self.value: Any = value
        self.hash: int = hash(key)
        self.next: Optional[Node] = None


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.table: list[Optional[Node]] = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._index_for_hash(hash(key))
        node = self.table[index]
        if node is None:
            self.table[index] = Node(key, value)
        else:
            while node:
                if node.key == key:
                    node.value = value
                    return
                if node.next is None:
                    node.next = Node(key, value)
                    break
                node = node.next
        self.size += 1
        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._index_for_hash(hash(key))
        node = self.table[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.size = 0
        self.table = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        index = self._index_for_hash(hash(key))
        node = self.table[index]
        prev: Optional[Node] = None
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.table[index] = node.next
                self.size -= 1
                return
            prev, node = node, node.next
        raise KeyError(f"Key {key} not found")

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable) -> Any:
        value = self[key]
        del self[key]
        return value

    def update(self, other: dict) -> None:
        for key in other:
            self[key] = other[key]

    def __iter__(self) -> Iterator[Any]:
        for node in self.table:
            while node:
                yield node.key
                node = node.next

    def _index_for_hash(self, hash_value: int) -> int:
        return hash_value % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            while node:
                self[node.key] = node.value
                node = node.next
