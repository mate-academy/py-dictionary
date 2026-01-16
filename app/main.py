from typing import Any, Optional, Iterator


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.value: Any = value
        self.hash: int = hash(key)


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 2 / 3,
    ) -> None:
        self._capacity: int = initial_capacity
        self._size: int = 0
        self._load_factor: float = load_factor
        self._table: list[Optional[Node]] = [None] * self._capacity

    def __len__(self) -> int:
        return self._size

    def _resize(self) -> None:
        old_table: list[Optional[Node]] = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size / self._capacity >= self._load_factor:
            self._resize()

        idx: int = hash(key) % self._capacity

        while self._table[idx] is not None:
            if self._table[idx].key == key:
                self._table[idx].value = value
                return
            idx = (idx + 1) % self._capacity

        self._table[idx] = Node(key, value)
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        idx: int = hash(key) % self._capacity

        while self._table[idx] is not None:
            if self._table[idx].key == key:
                return self._table[idx].value
            idx = (idx + 1) % self._capacity

        raise KeyError(key)

    def __iter__(self) -> Iterator[Any]:
        for node in self._table:
            if node is not None:
                yield node.key
