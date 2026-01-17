from typing import Hashable, Any, Optional, Iterator
from collections.abc import Mapping, Iterable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)
        self.next: Optional["Node"] = None


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.table: list[Optional[Node]] = [None] * self.capacity
        self.load_factor = 0.75

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index = hash(key) % self.capacity
        if self.table[index] is None:
            self.table[index] = Node(key, value)
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = Node(key, value)

        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        current = self.table[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"Key {key} not found")

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        current = self.table[index]
        prev = None

        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            prev, current = current, current.next

        raise KeyError(f"Key {key} not found")

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise

    def update(self,
               other: Mapping[Hashable, Any] | Iterable[tuple[Hashable, Any]]
               ) -> None:
        for key, value in other.items():
            self[key] = value

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def __iter__(self) -> Iterator[Hashable]:
        for i in range(self.capacity):
            current = self.table[i]
            while current:
                yield current.key
                current = current.next

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table: list[Optional[Node]] = [None] * new_capacity

        for i in range(self.capacity):
            current = self.table[i]
            while current:
                new_index = current.hash % new_capacity
                if new_table[new_index] is None:
                    new_table[new_index] = Node(current.key, current.value)
                else:
                    new_node = new_table[new_index]
                    while new_node.next:
                        new_node = new_node.next
                    new_node.next = Node(current.key, current.value)
                current = current.next

        self.table = new_table
        self.capacity = new_capacity
