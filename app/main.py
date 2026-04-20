from typing import Any, List, Tuple


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(capacity)]
        self._resizing: bool = False

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if not self._resizing and self.size / self.capacity > 0.75:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table

        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]

        self.size = 0
        self._resizing = True

        for bucket in old_table:
            for k, v in bucket:
                self[k] = v

        self._resizing = False
