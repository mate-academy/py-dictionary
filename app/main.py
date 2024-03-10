from typing import Any, Generator, Optional, Tuple, List, Hashable


class Dictionary:
    def __init__(
            self,
            capacity: int = 8
    ) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.table: List[Optional[Tuple[Any, int, Any]]] = (
            [None] * self.capacity
        )
        self.load_factor_threshold = 0.7

    def _hash(
            self,
            key: Hashable
    ) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node:
                self[node[0]] = node[2]

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if (
            self.size / self.capacity >= self.load_factor_threshold
        ):
            self._resize()

        index = self._hash(key)
        while (
                self.table[index] is not None and self.table[index][0] != key
        ):
            index = (index + 1) % self.capacity

        if self.table[index] is None:
            self.size += 1

        self.table[index] = (key, hash(key), value)

    def __getitem__(
            self,
            key: Hashable
    ) -> Any:
        index = self._hash(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __delitem__(
            self,
            key: Hashable
    ) -> None:
        index = self._hash(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = None
                self.size -= 1
                return
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def get(
            self,
            key: Hashable,
            default: Optional[Any] = None
    ) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(
            self
    ) -> Generator[Any, None, None]:
        for node in self.table:
            if node:
                yield node[0]
