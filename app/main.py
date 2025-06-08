from typing import Any, Iterator, Optional, Iterable, Union


class _Node:
    __slots__ = ("key", "value", "hash", "next")

    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)
        self.next: Optional[_Node] = None


class Dictionary:
    _INITIAL_CAPACITY = 8
    _LOAD_FACTOR = 0.7

    def __init__(self) -> None:
        self._capacity = self._INITIAL_CAPACITY
        self._size = 0
        self._buckets: list[Optional[_Node]] = [None] * self._capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._index_for_key(key)
        node = self._buckets[index]

        if node is None:
            self._buckets[index] = _Node(key, value)
            self._size += 1
        else:
            current = node
            while True:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = _Node(key, value)
            self._size += 1

        if self._size / self._capacity > self._LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._index_for_key(key)
        node = self._buckets[index]

        current = node
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"Key {repr(key)} not found.")

    def __len__(self) -> int:
        return self._size

    def _index_for_key(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for node in old_buckets:
            current = node
            while current is not None:
                self[current.key] = current.value
                current = current.next

    def clear(self) -> None:
        self._buckets = [None] * self._INITIAL_CAPACITY
        self._capacity = self._INITIAL_CAPACITY
        self._size = 0

    def __delitem__(self, key: Any) -> None:
        index = self._index_for_key(key)
        node = self._buckets[index]
        prev: Optional[_Node] = None
        current = node

        while current is not None:
            if current.key == key:
                if prev is None:
                    self._buckets[index] = current.next
                else:
                    prev.next = current.next
                self._size -= 1
                return
            prev = current
            current = current.next

        raise KeyError(f"Key {repr(key)} not found.")

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
            else:
                raise

    def update(self, other: Union[dict, Iterable[tuple[Any, Any]]]) -> None:
        if hasattr(other, "items"):
            for k, v in other.items():
                self[k] = v
        else:
            for k, v in other:
                self[k] = v

    def __iter__(self) -> Iterator[Any]:
        for node in self._buckets:
            current = node
            while current is not None:
                yield current.key
                current = current.next
