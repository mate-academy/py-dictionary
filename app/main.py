from app.point import Point
from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
# self.buckets = [None] * self.capacity
        self.buckets = [None for i in range(self.capacity)]

    def __setitem__(self, x: Any, y: Any) -> None:
        index = hash(x) % self.capacity
        if not self.buckets[index]:
            self.buckets[index] = Point(x, y)
        else:
            current = self.buckets[index]
            while current:
                if current.x == x:
                    current.y = y
                    return
                if not current.next:
                    current.next = Point(x, y)
                    break
                current = current.next
        self.size += 1

    def __getitem__(self, x: Any) -> None:
        index = hash(x) % self.capacity
        current = self.buckets[index]
        while current:
            if current.x == x:
                return current.y
            current = current.next
        raise KeyError(f"Key {x} not found")

    def __len__(self) -> Any:
        return self.size
