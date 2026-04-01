from app.point import Point
from typing import Any, List


class Node:

    def __init__(self, key: Any, hash_value: Any, value: Any) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value


class Dictionary:
    _DELETED = object()

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table: List[Any] = [None] * 8

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = hash(key)
        idx = hash_value % self.capacity

        while self.table[idx] is not None:
            if self.table[idx] is not self._DELETED:
                if self.table[idx].key == key:
                    self.table[idx].value = value
                    return
            idx = (idx + 1) % self.capacity

        new_node = Node(key, hash_value, value)
        self.table[idx] = new_node
        self.size += 1

        if self.size > self.capacity * 2 / 3:
            self._resize()

    def __getitem__(self, key: Any) -> Any:

        key_hash = hash(key)
        idx = key_hash % self.capacity

        while self.table[idx] is not None:
            if self.table[idx] is not self._DELETED:
                if self.table[idx].key == key:
                    return self.table[idx].value
            idx = (idx + 1) % self.capacity
        raise KeyError(f"Key {key} not found in Dictionary")

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None and node is not self._DELETED:
                self.__setitem__(node.key, node.value)

    def __len__(self) -> int:
        return self.size

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self.table = [None] * 8
        self.capacity = 8
        self.size = 0

    def __iter__(self) -> Any:
        for item in self.table:
            if item is not None and item is not self._DELETED:
                yield item.key

    def update(self, other: "Dictionary") -> None:
        for node in other.table:
            if node is not None and node is not other._DELETED:
                self[node.key] = node.value

    def __delitem__(self, key: Any) -> None:

        hash_value = hash(key)
        idx = hash_value % self.capacity

        while self.table[idx] is not None:
            node = self.table[idx]
            if node is not self._DELETED and node.key == key:
                self.table[idx] = self._DELETED
                self.size -= 1
                return
            idx = (idx + 1) % self.capacity
        raise KeyError(f"Key {key} not found for deletion")


my_dict = Dictionary()

p1 = Point(1, 2)
p2 = Point(3, 4)

my_dict[p1] = "A"
my_dict[p2] = "B"

print(my_dict[p1])
print(len(my_dict))
