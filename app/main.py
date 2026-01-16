from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        self.capacity *= 2
        self.size = 0
        old_table = self.hash_table
        self.hash_table = [None] * self.capacity

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self.resize()
        index = hash(key) % self.capacity

        while True:
            node = self.hash_table[index]

            if node is None:
                self.hash_table[index] = Node(key, value)
                self.size += 1
                return

            elif node.key == key:
                self.hash_table[index].value = value
                return

            index = (index + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity

        while True:
            node = self.hash_table[index]

            if node is None:
                raise KeyError(f"Key '{key}' not found, "
                               f"you're trying to find a value"
                               f"in a dict using a key that doesn't exist.")

            if node.key == key:
                return node.value

            index = (index + 1) % self.capacity
