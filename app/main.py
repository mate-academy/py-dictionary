from typing import Any


class Node:
    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.length: int = 0
        self.hash_table: list = [None] * self.capacity

    def _get_hash(self, key: Any) -> int:
        try:
            return hash(key)
        except TypeError:
            raise TypeError(f"key type:{type(key)} is not hashable")

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= (2 / 3) * self.capacity:
            self._resize()

        hash_value: int = self._get_hash(key)
        index: int = hash_value % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = Node(key, hash_value, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value: int = self._get_hash(key)
        index: int = hash_value % self.capacity
        start_index: int = index

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.capacity
            if index == start_index:
                break

        raise KeyError(f"jey '{key}' not found")

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table = [None] * self.capacity
