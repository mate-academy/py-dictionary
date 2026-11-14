from typing import Any, Hashable, Iterator


class Node:
    def __init__(
        self,
        key: Hashable,
        key_hash: int,
        value: Any,
    ) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.length = 0
        self.capacity = self.INITIAL_CAPACITY
        self.hash_table: list = [None] * self.capacity

    def _find_index(
        self,
        key: Hashable,
        key_hash: int,
    ) -> int:
        index = key_hash % self.capacity
        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.hash == key_hash and node.key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0
        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(
        self,
        key: Hashable,
        value: Any,
    ) -> None:
        key_hash = hash(key)
        index = self._find_index(key, key_hash)

        if self.hash_table[index] is not None:
            self.hash_table[index].value = value
            return

        self.hash_table[index] = Node(key, key_hash, value)
        self.length += 1

        if self.length > self.capacity * self.LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key, hash(key))
        if self.hash_table[index] is None:
            raise KeyError(f"Key {key!r} not found")
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        index = self._find_index(key, hash(key))
        if self.hash_table[index] is None:
            raise KeyError(f"Key {key!r} not found")

        self.hash_table[index] = None
        self.length -= 1

        next_index = (index + 1) % self.capacity
        while self.hash_table[next_index] is not None:
            node = self.hash_table[next_index]
            self.hash_table[next_index] = None
            self.length -= 1
            self[node.key] = node.value
            next_index = (next_index + 1) % self.capacity

    def clear(self) -> None:
        self.__init__()

    def get(
        self,
        key: Hashable,
        default: Any = None,
    ) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(
        self,
        key: Hashable,
        *default: Any,
    ) -> Any:
        try:
            value = self[key]
        except KeyError:
            if default:
                return default[0]
            raise
        del self[key]
        return value

    def update(self, other: Any) -> None:
        for key, value in other.items():
            self[key] = value

    def items(self) -> Iterator[tuple]:
        for node in self.hash_table:
            if node is not None:
                yield node.key, node.value

    def __iter__(self) -> Iterator:
        for key, _ in self.items():
            yield key
