from typing import Any, List, Tuple


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.table: List[
            List[Tuple[Any, int, Any]]
        ] = [[] for _ in range(capacity)]
        self._resizing: bool = False

    def _index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = self._index(key_hash)
        bucket = self.table[index]

        for i, (k, h, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, h, value)
                return

        bucket.append((key, key_hash, value))
        self.size += 1

        if not self._resizing and self.size / self.capacity > 0.75:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = self._index(key_hash)
        bucket = self.table[index]

        for k, h, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table

        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]

        self.size = 0
        self._resizing = True

        for bucket in old_table:
            for k, h, v in bucket:
                index = self._index(h)
                self.table[index].append((k, h, v))
                self.size += 1

        self._resizing = False
