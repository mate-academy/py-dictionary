from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor = 2 / 3
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        node = Node(key, value)
        index = node.hash % self.capacity
        while True:
            if not self.table[index]:
                self.table[index] = node
                self.size += 1
                break

            if (self.table[index].key == node.key
                    and self.table[index].hash == node.hash):
                self.table[index].value = node.value
                break

            index = (index + 1) % self.capacity

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        item = self.table[index]

        while item:
            if item.key == key and item.hash == hash(key):
                return item.value

            index = (index + 1) % self.capacity
            item = self.table[index]

        raise KeyError("Can't find key: " + key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity

        for node in self.table:
            if node:
                index = node.hash % self.capacity
                while new_table[index]:
                    index = (index + 1) % self.capacity
                new_table[index] = node

        self.table = new_table
