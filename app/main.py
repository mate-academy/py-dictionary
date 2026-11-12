from typing import Any, Hashable, Iterator


_DELETED = object()
_MISSING = object()


class Node:
    def __init__(self, key: Hashable, key_hash: int, value: Any) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3
    RESIZE_MULTIPLIER = 2

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._hash_table: list = [None] * self._capacity
        self._length = 0
        self._deleted = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self._capacity
        first_deleted = None

        while self._hash_table[index] is not None:
            node = self._hash_table[index]
            if node is _DELETED:
                if first_deleted is None:
                    first_deleted = index
            elif node.hash == key_hash and node.key == key:
                node.value = value
                return
            index = (index + 1) % self._capacity

        if first_deleted is not None:
            index = first_deleted
            self._deleted -= 1

        self._hash_table[index] = Node(key, key_hash, value)
        self._length += 1

        if self._length + self._deleted > self._capacity * self.LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key)
        if index is None:
            raise KeyError(f"Key {key!r} is not in the dictionary")
        return self._hash_table[index].value

    def __len__(self) -> int:
        return self._length

    def __delitem__(self, key: Hashable) -> None:
        index = self._find_index(key)
        if index is None:
            raise KeyError(f"Key {key!r} is not in the dictionary")
        self._hash_table[index] = _DELETED
        self._length -= 1
        self._deleted += 1

    def __iter__(self) -> Iterator:
        for node in self._hash_table:
            if node is not None and node is not _DELETED:
                yield node.key

    def clear(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._hash_table = [None] * self._capacity
        self._length = 0
        self._deleted = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        index = self._find_index(key)
        if index is None:
            return default
        return self._hash_table[index].value

    def pop(self, key: Hashable, default: Any = _MISSING) -> Any:
        index = self._find_index(key)
        if index is None:
            if default is _MISSING:
                raise KeyError(f"Key {key!r} is not in the dictionary")
            return default
        value = self._hash_table[index].value
        del self[key]
        return value

    def update(self, other: Any = ()) -> None:
        if isinstance(other, Dictionary) or hasattr(other, "keys"):
            for key in other:
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value

    def _find_index(self, key: Hashable) -> int | None:
        key_hash = hash(key)
        index = key_hash % self._capacity

        while self._hash_table[index] is not None:
            node = self._hash_table[index]
            if (
                node is not _DELETED
                and node.hash == key_hash
                and node.key == key
            ):
                return index
            index = (index + 1) % self._capacity

        return None

    def _resize(self) -> None:
        old_table = self._hash_table
        if self._length > self._capacity * self.LOAD_FACTOR / 2:
            self._capacity *= self.RESIZE_MULTIPLIER
        self._hash_table = [None] * self._capacity
        self._deleted = 0

        for node in old_table:
            if node is None or node is _DELETED:
                continue
            index = node.hash % self._capacity
            while self._hash_table[index] is not None:
                index = (index + 1) % self._capacity
            self._hash_table[index] = node
