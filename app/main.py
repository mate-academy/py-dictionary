from typing import Any, Hashable


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3
    RESIZE_MULTIPLIER = 2

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.hash_table: list = [None] * self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        """Find index for the key: its own cell or the first free one."""
        index = hash(key) % self.capacity

        while (
            self.hash_table[index] is not None
            and self.hash_table[index][0] != key
        ):
            index = (index + 1) % self.capacity

        return index

    def _resize(self) -> None:
        """Double the capacity and rehash all existing nodes."""
        old_hash_table = self.hash_table

        self.capacity *= self.RESIZE_MULTIPLIER
        self.size = 0
        self.hash_table = [None] * self.capacity

        for node in old_hash_table:
            if node is not None:
                self[node[0]] = node[2]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            self.size += 1

        self.hash_table[index] = (key, hash(key), value)

        if self.size > self.capacity * self.LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Key '{key}' not found in the dictionary")

        return self.hash_table[index][2]

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.hash_table = [None] * self.capacity

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self) -> Any:
        for node in self.hash_table:
            if node is not None:
                yield node[0]

    def update(self, other: "Dictionary") -> None:
        for key in other:
            self[key] = other[key]

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Key '{key}' not found in the dictionary")

        self.hash_table[index] = None
        self.size -= 1
        index = (index + 1) % self.capacity

        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            self.hash_table[index] = None
            self.size -= 1
            self[node[0]] = node[2]
            index = (index + 1) % self.capacity

    def pop(self, key: Hashable, *args: Any) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if args:
                return args[0]
            raise
