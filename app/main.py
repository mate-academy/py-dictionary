from typing import Hashable, Any, Optional


class Node:
    def __init__(self, key: Hashable, hash_: int, value: Any) -> None:
        self.key = key
        self.hash_ = hash_
        self.value = value


class Dictionary:
    INITIAL_CAPACITY: int = 8
    LOAD_FACTOR: float = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self.length = 0
        self.hash_table = [None] * self.capacity

    def _get_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self.capacity

        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    def _resize(self) -> None:
        old_hash_table: list[Optional[Node]] = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_hash_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length / self.capacity >= self.LOAD_FACTOR:
            self._resize()

        index: int = self._get_index(key)
        if self.hash_table[index] is None:
            self.length += 1
        self.hash_table[index] = Node(key, hash(key), value)

    def __getitem__(self, key: Hashable) -> Any:
        index: int = self._get_index(key)
        if self.hash_table[index] is None:
            raise KeyError(f"Key not found: {key}")
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.length
