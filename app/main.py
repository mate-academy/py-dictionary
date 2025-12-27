from typing import Any


class Node:
    def __init__(
            self,
            key: Any,
            hashcode: int,
            value: Any
    ) -> None:
        self.key = key
        self.hash = hashcode
        self.value = value


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 2 / 3
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [None] * self.capacity

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def _find_slot(
            self,
            key: Any,
            hashcode: int
    ) -> int:
        index = hashcode % self.capacity
        start_index = index
        while True:
            node = self.table[index]

            if node is None or node.key == key:
                return index

            index = (index + 1) % self.capacity
            if index == start_index:
                raise RuntimeError("Hashtable is full")

    def __setitem__(
            self,
            key: Any,
            value: Any
    ) -> None:
        hashcode = hash(key)
        slot = self._find_slot(key, hashcode)

        if self.table[slot] is None:
            self.table[slot] = Node(key, hashcode, value)
            self.size += 1
        else:
            self.table[slot].value = value

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hashcode = hash(key)
        index = hashcode % self.capacity
        start = index

        while True:
            node = self.table[index]

            if node is None:
                raise KeyError(key)

            if node.key == key:
                return node.value

            index = (index + 1) % self.capacity

            if index == start:
                raise KeyError(key)

    def __len__(self) -> int:
        return self.size
