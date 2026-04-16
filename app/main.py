from typing import Any, Optional, List, Tuple


class Dictionary:

    def __init__(self, capacity: int = 8) -> None:
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")

        self.capacity: int = capacity
        self.size: int = 0
        self.load_factor: float = 2 / 3
        self.table: List[Optional[Tuple[Any, int, Any]]] = (
            [None] * self.capacity
        )

    def _hash(self, key: Any) -> int:
        return hash(key)

    def _find_slot(self, key: Any, f_hash: int) -> int:
        index: int = f_hash % self.capacity
        while self.table[index] is not None:
            node = self.table[index]
            if (node is not None
                    and node[1] == f_hash
                    and node[0] == key):
                return index
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        f_hash: int = self._hash(key)
        index: int = self._find_slot(key, f_hash)

        if self.table[index] is None:
            self.size += 1

        self.table[index] = (key, f_hash, value)

    def __getitem__(self, key: Any) -> Any:
        f_hash: int = self._hash(key)
        index: int = self._find_slot(key, f_hash)
        node = self.table[index]

        if (node is not None
                and node[1] == f_hash
                and node[0] == key):
            return node[2]

        raise KeyError(f"Key {key} not found")

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None:
                idx = self._find_slot(item[0], item[1])
                self.table[idx] = item
                self.size += 1

    def __len__(self) -> int:
        return self.size
