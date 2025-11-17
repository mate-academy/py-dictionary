from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:

    def __init__(self, capacity: int = 8, load_factor: float = 0.7) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._calculate_index(hash(key))

        if self.table[index] is None:
            self.table[index] = []

        for node in self.table[index]:
            if node.key == key:
                node.value = value
                return

        new_node = Node(key, value)

        self.table[index].append(new_node)

        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._calculate_index(hash(key))

        if self.table[index] is None:
            raise KeyError

        for node in self.table[index]:
            if node.key == key:
                return node.value

        raise KeyError

    def __len__(self) -> int:
        return self.size

    def _calculate_index(self, hash_value: int) -> int:
        return hash_value % self.capacity

    def _resize(self) -> None:
        self.capacity *= 2
        old_table = self.table
        self.table = [None] * self.capacity
        self.size = 0

        for bucket in old_table:
            if bucket is None:
                continue

            for node in bucket:
                self.__setitem__(node.key, node.value)
