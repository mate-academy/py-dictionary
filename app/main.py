from typing import Any, Optional, Iterator
from dataclasses import dataclass

from app.point import Point


@dataclass
class Node:
    key: Any
    value: Any
    node_hash: int


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 2 / 3) -> None:
        self.capacity: int = initial_capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.table: list[Optional[Node]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        hash_value: int = hash(key)
        index: int = hash_value % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                # Update existing key
                self.table[index].value = value
                return
            # Linear probing
            index = (index + 1) % self.capacity

        # Insert new key-value pair
        self.table[index] = Node(key, value, hash_value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found in dictionary.")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity: int = self.capacity * 2
        new_table: list[Optional[Node]] = [None] * new_capacity

        # Rehash all items into the new table
        for node in self.table:
            if node is not None:
                index: int = node.node_hash % new_capacity
                while new_table[index] is not None:
                    index = (index + 1) % new_capacity
                new_table[index] = node

        self.table = new_table
        self.capacity = new_capacity

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        hash_value: int = hash(key)
        index: int = hash_value % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index] = None
                self.size -= 1
                return
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found in dictionary.")

    def get(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"Key '{key}' not found in dictionary.")

    def __iter__(self) -> Iterator[Any]:
        for node in self.table:
            if node is not None:
                yield node.key


first_point = Point(3.4, 8.5)
second_point = Point(4.5, 8.5)
print(first_point, second_point)

print(first_point.__eq__(second_point))
print(first_point.__hash__())
print(second_point.__hash__())
third_point = Point(8.4, 8.5)
print(first_point.__eq__(third_point))
print(third_point.__hash__())
points = Dictionary()
points.__setitem__(first_point, 11.9)
print(points.__getitem__(first_point))
points.__setitem__(second_point, 15)
points.__setitem__(third_point, 11.9)
print(points.__getitem__(second_point))
print(points.__getitem__(third_point))
print(points.__len__())
points.__setitem__(first_point, 3.4)
print(points.__getitem__(first_point))
print(points.__len__())
print(points.__iter__())
forth_point = Point(3.4, 8.6)
fifth_point = Point(3.9, 8.5)
sixth_point = Point(3.8, 8.5)
seventh_point = Point(3.8, 2.5)
points.__setitem__(forth_point, 10)
points.__setitem__(fifth_point, 76)
points.__setitem__(sixth_point, 66)
points.__setitem__(seventh_point, 67)
print(points.__len__())
print(points.table)
print(points.__getitem__(first_point))
