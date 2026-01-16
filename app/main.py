from typing import Any, Optional, Hashable, Iterator


class Node:
    def __init__(self, key: Hashable, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value
        self.next: Optional[Node] = None


class Dictionary:
    def __init__(self, initial_capacity: int = 16,
                 load_factor: float = 0.75) -> None:
        self.capacity = initial_capacity
        self.table: list[Optional[Node]] = [None] * self.capacity
        self.size: int = 0
        self.load_factor = load_factor

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: Hashable) -> bool:
        index = hash(key) % self.capacity
        current = self.table[index]
        while current:
            if current.key == key:
                return True
            current = current.next
        return False

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        if self.table[index] is None:
            self.table[index] = Node(key, hash_value, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = Node(key, hash_value, value)
            self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize(self.capacity * 2)

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index = hash_value % self.capacity
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity
        current = self.table[index]
        prev: Optional[Node] = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            prev = current
            current = current.next
        raise KeyError(key)

    def __iter__(self) -> Iterator[Hashable]:
        for bucket in self.table:
            current = bucket
            while current:
                yield current.key
                current = current.next

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = ...) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not ...:
                return default
            raise KeyError(key)

    def update(self, other: Optional[dict[Hashable, Any]] = None,
               **kwargs: Any) -> None:
        if other:
            if isinstance(other, Dictionary):
                for key in other:
                    self[key] = other[key]
            elif isinstance(other, dict):
                for key, value in other.items():
                    self[key] = value
            elif hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            else:
                try:
                    for key, value in other:
                        self[key] = value
                except TypeError:
                    raise TypeError("update expected dictionary "
                                    "or iterable with (key, value) pairs")
        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def _resize(self, new_capacity: int) -> None:
        old_table = self.table
        self.capacity = new_capacity
        self.table = [None] * self.capacity
        self.size = 0
        for bucket in old_table:
            current = bucket
            while current:
                self[current.key] = current.value
                current = current.next
