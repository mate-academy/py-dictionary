from fractions import Fraction
from typing import Any, Hashable, Iterable


class Dictionary:
    class Node:
        def __init__(self, key: Hashable, value: Any, hash_num: int) -> None:
            self.key = key
            self.value = value
            self.hash_num = hash_num

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity
        self.load_factor = Fraction(2, 3)

    def __str__(self) -> str:
        return f"{self.table}"

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)
        index = self.find_index(index, key)
        if index[1]:
            self.table[index[0]].value = value
            return

        self.table[index[0]] = self.Node(key, value, hash(key))
        self.size += 1
        if self.size / self.capacity >= self.load_factor:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        index = self.find_index(index, key)

        if not index[1]:
            raise KeyError(f"Requested key '{key}' "
                           f"is not found in a dictionary")

        return self.table[index[0]].value

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)
        index = self.find_index(index, key)

        if index[1]:
            self.table[index[0]] = None
            self.size -= 1
            self.rehash()
        else:
            raise KeyError("Сan`t delete a key that "
                           "does not exist in a dictionary")

    def get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def find_index(
            self,
            index: int,
            key: Hashable
    ) -> tuple[int | Any, bool] | None:
        while self.table[index] is not None:
            if self.table[index].key == key:
                return index, True
            index = (index + 1) % self.capacity
        return index, False

    def resize(self) -> None:
        old_table = self.table[:]
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def rehash(self) -> None:
        old_table = self.table[:]
        self.table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is not None:
                self[node.key] = node.value

    def __iter__(self) -> list:
        return (node.key for node in self.table if node is not None)

    def update(self, other: dict | Iterable) -> None:
        if hasattr(other, "items"):
            items = other.items()
        else:
            items = other

        try:
            for key, value in items:
                self.__setitem__(key, value)
        except TypeError:
            raise ValueError("The input must be a dictionary "
                             "or an iterable of key-value pairs")

    def pop(self, key: Hashable, default: Any = None) -> Any:
        index = self.get_index(key)
        index = self.find_index(index, key)

        if index[1]:
            value = self.table[index[0]].value
            self.table[index[0]] = None
            self.size -= 1
            self.rehash()
            return value

        if default is not None:
            return default

        raise KeyError(f"Requested key '{key}' is not found in a dictionary")

    def clear(self) -> None:
        self.table = [None] * self.capacity
