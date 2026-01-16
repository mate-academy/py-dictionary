from typing import Any, Hashable


class Dictionary:

    def __init__(self) -> None:
        self.capacity: int = 8
        self.size: int = 0
        self.table: (list)[list[tuple[Hashable, Any]]]
        self.table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size
