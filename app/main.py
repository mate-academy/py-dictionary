from typing import Any

from typing import Iterator


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, size: int = 8, load_factor: float = 0.66) -> None:
        self.size = size
        self.load_factor = load_factor
        self.table = [[] for _ in range(self.size)]
        self.count = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.count / self.size > self.load_factor:
            self._resize()
        index = hash(key) % self.size
        for node in self.table[index]:
            if node.key == key:
                node.value = value
                return
        self.table[index].append(Node(key, value))
        self.count += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.size
        for node in self.table[index]:
            if node.key == key:
                return node.value
        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.count

    def _resize(self) -> None:
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        for block in old_table:
            for node in block:
                self.__setitem__(node.key, node.value)

    def clear(self) -> None:
        self.table = [[] for _ in range(self.size)]
        self.count = 0

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.size
        block = self.table[index]
        for i, node in enumerate(block):
            if node.key == key:
                del block[i]
                self.count -= 1
                return
        raise KeyError(f"Key {key} not found.")

    def get(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % self.size
        for node in self.table[index]:
            if node.key == key:
                return node.value
        return default

    def pop(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % self.size
        block = self.table[index]
        for i, node in enumerate(block):
            if node.key == key:
                value = node.value
                del block[i]
                self.count -= 1
                return value
        if default is not None:
            return default
        raise KeyError(f"Key {key} not found.")

    def update(self, other: "Dictionary") -> None:
        for block in other.table:
            for node in block:
                self.__setitem__(node.key, node.value)

    def __iter__(self) -> Iterator[Any]:
        for block in self.table:
            for node in block:
                yield node.key
