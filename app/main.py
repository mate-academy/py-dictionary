from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.load_factor: float = 0.75
        self.size: int = 0
        self.hash_table: list = [None] * self.capacity

    class Node:
        def __init__(self, key: Hashable, value: Any, hash_code: int) -> None:
            self.key: Hashable = key
            self.value: Any = value
            self.hash_code: int = hash_code

    def _hash(self, key: Hashable) -> int:
        return hash(key)

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_hash_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()

        hash_code = self._hash(key)
        index = hash_code % self.capacity
        new_node = self.Node(key, value, hash_code)

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = new_node
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_code = self._hash(key)
        index = hash_code % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not in Dictionary")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        hash_code = self._hash(key)
        index = hash_code % self.capacity

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index] = None
                self.size -= 1
                return
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not in Dictionary")

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self.__setitem__(key, value)

    def __iter__(self) -> None:
        for node in self.hash_table:
            if node is not None:
                yield node.key
