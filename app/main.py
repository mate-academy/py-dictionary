from typing import Hashable

INITIAL_CAPACITY = 8
RESIZE_THRESHOLD = 2 / 3
CAPACITY_MULTIPLIER = 2


class Node:
    def __init__(self, key: Hashable, value: any) -> None:
        self.key = key
        self.value = value
        self.next = None

    def __str__(self) -> str:
        return f"({self.key}, {self.value})"

    def __repr__(self) -> str:
        return self.__str__()


class Dictionary:
    def __init__(self) -> None:
        self.capacity = INITIAL_CAPACITY
        self.size = 0
        self.load_factor = RESIZE_THRESHOLD
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: any) -> None:
        index = self._calculate_index(key)
        node = self.table[index]

        if node is None:
            if self.size + 1 >= self.capacity * self.load_factor:
                self.resize()
                return self.__setitem__(key, value)
            self.size += 1
        self.table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> str:
        index = self._calculate_index(key)

        if self.table[index] is None:
            raise KeyError(f"Key {key} not found")

        return self.table[index].value

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def resize(self) -> None:
        old_hash_table = self.table
        self.capacity *= CAPACITY_MULTIPLIER
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __delitem__(self, key: Hashable) -> None:
        index = self.hash(key)
        node = self.table[index]
        if node is None:
            raise KeyError(f"Key {key} not found")
        if node.key == key:
            self.table[index] = node.next
            self.size -= 1
            return
        prev = node
        while node:
            if node.key == key:
                prev.next = node.next
                self.size -= 1
                return
            prev = node
            node = node.next
        raise KeyError(f"Key {key} not found")

    def get(self, key: Hashable, default: None = None) -> any:
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self) -> any:
        for node in self.table:
            while node:
                yield node.key
                node = node.next

    def _calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (self.table[index] is not None and self.table[index].key != key):
            index = (index + 1) % self.capacity

        return index

    def __str__(self) -> str:
        return str(self.table)
