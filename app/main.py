from typing import Any


class Node:
    def __init__(self, key: Any, value: Any, hash_value: int) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.table: list[Node | None] = [None] * self.capacity
        self.load_factor = 2 / 3

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.table[index] is not None:
            node = self.table[index]
            if node and node.key == key:
                node.value = value
                return
            index = (index + 1) % self.capacity

        self.table[index] = Node(key, value, key_hash)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        start_index = index

        while self.table[index] is not None:
            node = self.table[index]
            if node and node.key == key:
                return node.value

            index = (index + 1) % self.capacity
            if index == start_index:
                break

        raise KeyError(f"Key {key} not found.")

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __repr__(self) -> str:
        items = [f"{n.key}: {n.value}" for n in self.table if n]
        return "{" + ", ".join(items) + "}"
