from typing import Any
from app.point import Point


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.table: list[list[tuple[Any, Any]]] = [
            [] for _ in range(self.capacity)
        ]

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % self.capacity
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > 0.7:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_table:
            for k, v in bucket:
                self[k] = v


p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(2, 3)

d = Dictionary()
d[p1] = "first"
d[p2] = "second"
d[p3] = "third"

print(d[p1])
print(d[p2])
print(d[p3])
print(len(d))
