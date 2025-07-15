from typing import Any, Optional, List


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self. hash = hash(key)


class Dictionary:
    def __init__(self, capacity: int = 1) -> None:
        self.capacity = capacity
        self.size = 0
        self._data: List[Optional[List[Node]]] = [None] * capacity

    def load_factor(self) -> float:
        return self.size / self.capacity

    def needs_resize(self) -> bool:
        return self.load_factor() > 0.75

    def _resize(self) -> None:
        old_data = self._data
        self.capacity *= 2
        self._data = [None] * self.capacity
        self.size = 0

        for bucket in old_data:
            if bucket:
                for node in bucket:
                    self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.needs_resize():
            self._resize()

        index = hash(key) % self.capacity
        if self._data[index] is None:
            self._data[index] = []

        for node in self._data[index]:
            if node.key == key:
                node.value = value
                return

        self._data[index].append(Node(key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        bucket = self._data[index]

        if bucket is None:
            raise KeyError(key)

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
