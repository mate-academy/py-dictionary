from typing import Any, Hashable


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * self.capacity
        self.load_factor = 0.75

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()
        index = self._hash(key)
        node = self.table[index]
        if node is None:
            self.table[index] = [(key, value)]
            self.size += 1
        else:
            for i, (k, v) in enumerate(node):
                if k == key:
                    node[i] = (key, value)
                    return
            node.append((key, value))
            self.size += 1

    def __getitem__(self, key: Hashable) -> None:
        index = self._hash(key)
        node = self.table[index]

        if node is not None:
            for k, v in node:
                if k == key:
                    return v
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        self.capacity *= 2
        old_table = self.table
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                for key, value in node:
                    self.__setitem__(key, value)

    def __delitem__(self, key: Hashable) -> None:
        index = self._hash(key)
        node = self.table[index]
        if node is None:
            raise KeyError(f"Key '{key}' not found")
        for i, (k, v) in enumerate(node):
            if k == key:
                del node[i]
                self.size -= 1
                if not node:
                    self.table[index] = None
                return
        raise KeyError(f"Key '{key}' not found")
