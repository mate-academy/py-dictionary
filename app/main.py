from typing import Hashable, Any

from app.node import Node


class Dictionary:
    def __init__(self, *args, **kwargs) -> None:
        self.size = 0
        self.capacity = 8
        self.buckets = [None] * self.capacity
        self.threshold_load_factor = 0.75

        # we can pass tuples (key, value) when creating a Dictionary
        for key, value in args:
            self[key] = value

    def _hash(self, key: Hashable) -> tuple[int, int]:
        hash_value = hash(key)
        index = hash_value % self.capacity
        return hash_value, index

    def _find_node(self, key: Hashable) -> tuple[None, Node | None, int]:
        hash_value, index = self._hash(key)
        current = self.buckets[index]
        previous = None

        while current is not None:
            if current.key == key:
                return current, previous, index
            previous = current
            current = current.next_node

        return None, previous, index

    def _resize(self) -> None:
        old_buckets = self.buckets
        old_capacity = self.capacity

        self.capacity *= 2
        self.size = 0
        self.buckets = [None] * self.capacity

        for i in range(old_capacity):
            current = old_buckets[i]
            while current is not None:
                next_node = current.next_node
                self[current.key] = current.value
                current = next_node

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.threshold_load_factor:
            self._resize()

        hash_value, index = self._hash(key)
        current = self.buckets[index]

        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next_node

        new_node = Node(key, value, hash_value)
        new_node.next_node = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

    def __getitem__(self, key: Hashable) -> None:
        node, _, _ = self._find_node(key)

        if node is not None:
            return node.value
        raise KeyError(f"Key '{key}' not found")

    def __delitem__(self, key: Hashable) -> None:
        node, previous, index = self._find_node(key)
        if node is None:
            raise KeyError(f"Key '{key}' not found")

        if previous is None:
            self.buckets[index] = node.next_node
        else:
            previous.next_node = node.next_node

        self.size -= 1

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Any:
        for i in range(self.capacity):
            current = self.buckets[i]
            while current is not None:
                yield current.key
                current = current.next_node

    def get(self, key: Hashable, default: Any = None) -> Any | None:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any | None:
        try:
            value = self[key]
            self.__delitem__(key)
            return value
        except KeyError:
            if default is None:
                raise
            return default

    def clear(self) -> None:
        self.buckets = [None] * self.capacity
        self.size = 0

    def keys(self) -> list[Hashable]:
        return list(self)

    def values(self) -> list[Any]:
        return [self[key] for key in self]

    def items(self) -> list[tuple[Hashable, Any]]:
        items = []
        for i in range(self.capacity):
            current = self.buckets[i]
            while current is not None:
                items.append((current.key, current.value))
                current = current.next_node
        return items

    def __repr__(self) -> str:
        result = []
        for key, value in self.items():
            result.append(f"{str(key)}: {str(value)}")
        return "{" + ", ".join(result) + "}"
