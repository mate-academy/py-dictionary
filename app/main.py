from typing import Any, Iterator

_sentinel = object()


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self._size = 0
        self._capacity = initial_capacity
        self._buckets = [None] * self._capacity
        self._load_factor = 2 / 3

    def __len__(self) -> int:
        return self._size

    def __getitem__(self, key: Any) -> Any:
        hash_calculated = hash(key)
        index = hash_calculated % self._capacity
        node = self._buckets[index]

        while node is not None:
            if node.key == key:
                return node.value
            node = node.next

        raise KeyError(f"Key not found: {key!r}")

    def __setitem__(self, key: Any, value: Any) -> None:

        if self._needs_resize():
            self.resize()

        self._insert_no_resize(key, value)

    def _insert_no_resize(self, key: Any, value: Any) -> None:
        hash_calculated = hash(key)
        index = hash_calculated % self._capacity

        if self._buckets[index] is None:
            self._buckets[index] = Node(key, hash_calculated, value, )
            self._size += 1
        else:
            node = self._buckets[index]
            while node is not None:
                if node.key == key:
                    node.value = value
                    return
                node = node.next
            new_node = Node(key, hash_calculated, value)
            new_node.next = self._buckets[index]
            self._buckets[index] = new_node
            self._size += 1

    def _needs_resize(self) -> bool:
        return (self._size + 1) > (self._capacity * self._load_factor)

    def resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for bucket in old_buckets:
            node = bucket
            while node is not None:
                self._insert_no_resize(node.key, node.value)
                node = node.next

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._size = 0

    def __delitem__(self, key: Any) -> None:
        hash_calculated = hash(key)
        index = hash_calculated % self._capacity
        node = self._buckets[index]
        prev = None

        while node is not None:
            if node.key == key:
                if prev is None:
                    self._buckets[index] = node.next
                else:
                    prev.next = node.next
                self._size -= 1
                return
            prev = node
            node = node.next

        raise KeyError(f"Key not found: {key!r}")

    def get(self, key: Any, default: Any = None) -> Any:
        hash_calculated = hash(key)
        index = hash_calculated % self._capacity
        node = self._buckets[index]

        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        return default

    def pop(self, key: Any, default: Any = _sentinel) -> Any:
        hash_calculated = hash(key)
        index = hash_calculated % self._capacity
        node = self._buckets[index]
        prev = None

        while node is not None:
            if node.key == key:
                value = node.value

                if prev is None:
                    self._buckets[index] = node.next
                else:
                    prev.next = node.next

                self._size -= 1
                return value

            prev = node
            node = node.next

        if default is not _sentinel:
            return default

        raise KeyError(f"Key not found: {key!r}")

    def update(self, other: Any) -> None:
        if hasattr(other, "items"):
            iterable = other.items()
        else:
            iterable = other

        for key, value in iterable:
            self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for bucket in self._buckets:
            node = bucket
            while node is not None:
                yield node.key
                node = node.next


class Node:
    __slots__ = ("key", "hash", "value", "next")

    def __init__(
            self,
            key: Any,
            hash_calculated: int,
            value: Any,
            next_node: None = None
    ) -> None:
        self.key = key
        self.hash = hash_calculated
        self.value = value
        self.next = next_node
