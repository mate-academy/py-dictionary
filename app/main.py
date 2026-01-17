from typing import Any, Iterator


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self, initial_capacity: int = 8,
                 load_factor: float = 0.75) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        index = hash(key) % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = Node(key, value)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} not found")

    def __iter__(self) -> Iterator:
        for node in self.hash_table:
            if node:
                yield node.key

    def __len__(self) -> int:
        return self.size

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self.__setitem__(key, value)

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for node in self.hash_table:
            if node:
                index = node.hash % new_capacity
                while new_table[index] is not None:
                    index = (index + 1) % new_capacity
                new_table[index] = node

        self.capacity = new_capacity
        self.hash_table = new_table

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index] = None
                self.size -= 1
                self._rehash(index)
                return
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} not found")

    def _rehash(self, index: int) -> None:
        next_index = (index + 1) % self.capacity

        while self.hash_table[next_index] is not None:
            node = self.hash_table[next_index]
            self.hash_table[next_index] = None
            self.size -= 1

            self.__setitem__(node.key, node.value)
            next_index = (next_index + 1) % self.capacity
