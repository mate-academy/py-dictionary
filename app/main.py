from typing import Any, Hashable


class Dictionary:

    class Node:
        def __init__(self, key: Hashable, value: Any) -> None:
            self.key = key
            self.value = value
            self.hash = hash(key)

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def resize(self) -> None:
        new_capacity = self.capacity * 2
        new_hash_table = [None] * new_capacity

        for bucket in self.hash_table:
            if bucket is not None:
                for node in bucket:
                    new_index = node.hash % new_capacity
                    if new_hash_table[new_index] is None:
                        new_hash_table[new_index] = []
                    new_hash_table[new_index].append(node)

        self.hash_table = new_hash_table
        self.capacity = new_capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self.resize()

        index = self.index(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = []

        for node in self.hash_table[index]:
            if node.key == key:
                node.value = value
                return

        self.hash_table[index].append(self.Node(key, value))
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self.index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Key '{key}' not found.")

        for node in self.hash_table[index]:
            if node.key == key:
                return node.value

        raise KeyError(f"Key '{key}' not found.")

    def __delitem__(self, key: Hashable) -> None:
        index = self.index(key)

        if self.hash_table[index] is None:
            raise KeyError(f"Key '{key}' not found.")

        for i, node in enumerate(self.hash_table[index]):
            if node.key == key:
                del self.hash_table[index][i]
                self.size -= 1
                return

        raise KeyError(f"Key '{key}' not found.")
