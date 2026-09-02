from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, hash_val: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_val


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.table: list[Node | None] = [None] * self.capacity
        self.size = 0
        self.load_factor_threshold = 2 / 3

    def __len__(self) -> int:
        return self.size

    def _get_index(self, hash_val: int) -> int:
        return hash_val % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_val = hash(key)
        index = self._get_index(hash_val)

        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index].value = value
                return

            index = (index + 1) % self.capacity

        self.table[index] = Node(key, value, hash_val)
        self.size += 1

        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_val = hash(key)
        index = self._get_index(hash_val)

        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value

            index = (index + 1) % self.capacity

        raise KeyError(key)

    def _resize(self) -> None:
        old_table = self.table
        self.capacity = self.capacity * 2
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            if node is not None:
                self[node.key] = node.value
