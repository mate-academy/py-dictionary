from typing import Any, Hashable


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, default_capacity: int = 8,
                 load_factor: float = 0.66) -> None:
        self.capacity = default_capacity
        self.load_factor = load_factor
        self.size = 0
        self._data = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self._resize()
        h = hash(key)
        index = h % self.capacity
        while self._data[index] is not None:
            node = self._data[index]
            if node.hash == h and node.key == key:
                node.value = value
                return
            index = (index + 1) % self.capacity

        self._data[index] = Node(key, value)
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        h = hash(key)
        index = h % self.capacity
        while self._data[index] is not None:
            node = self._data[index]
            if node.hash == h and node.key == key:
                return node.value
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_data = self._data
        self.capacity *= 2
        self._data = [None] * self.capacity
        for node in old_data:
            if node is not None:
                index = node.hash % self.capacity
                while self._data[index] is not None:
                    index = (index + 1) % self.capacity
                self._data[index] = node
