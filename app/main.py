from typing import Any, Optional, Iterator


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash: int = hash(key)
        self.next: Optional["Node"] = None  # для колізій (ланцюжки)


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.load_factor: float = load_factor
        self.table: list[Optional[Node]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index: int = hash(key) % self.capacity
        node: Optional[Node] = self.table[index]

        if node is None:
            self.table[index] = Node(key, value)
            self.size += 1
            return

        prev: Optional[Node] = None
        while node:
            if node.key == key:
                node.value = value
                return
            prev = node
            node = node.next

        assert prev is not None
        prev.next = Node(key, value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index: int = hash(key) % self.capacity
        node: Optional[Node] = self.table[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            while node:
                self[node.key] = node.value
                node = node.next

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        index: int = hash(key) % self.capacity
        node: Optional[Node] = self.table[index]
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

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self) -> Iterator[Any]:
        for bucket in self.table:
            node = bucket
            while node:
                yield node.key
                node = node.next
