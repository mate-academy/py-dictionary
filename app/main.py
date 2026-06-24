from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table: list[Node | None] = [None] * self.capacity

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= 2 / 3:
            self.resize()
        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index].key == key:
                self.table[index].value = value
                return
            index = (index + 1) % self.capacity
        self.table[index] = Node(key, value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index].key == key:
                return self.table[index].value
            index = (index + 1) % self.capacity
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.size
