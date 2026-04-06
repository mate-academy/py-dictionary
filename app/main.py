from typing import Any


class Node:
    def __init__(self, key: Any,
                 value: Any, hash_val: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_val


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.length = 0
        self.table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * (2 / 3):
            self._resize()

        hash_val = hash(key)
        index = hash_val % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.table[index] = Node(key, value, hash_val)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity

        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} not found")
