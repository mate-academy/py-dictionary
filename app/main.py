from __future__ import annotations
from typing import Hashable, Iterable, Iterator, Any


class Dictionary:
    def __init__(
            self,
            iterable: Iterable = None,
            **kwargs: Iterable
    ) -> None:

        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]
        if iterable:
            for key, value in iterable:
                self[key] = value
        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def items(self) -> Iterator:
        return iter([value[0], value[1]] for value in self.hash_table if value)

    def keys(self) -> Iterator:
        return iter(value[0] for value in self.hash_table if value)

    def get(
            self,
            key: Hashable,
            default: None
    ) -> Any:

        try:
            return self[key]
        except KeyError:
            return default

    def pop(
            self,
            key: Hashable,
            default: Hashable = None
    ) -> Any:
        try:
            value = self.hash_table[self.find_index(key)][1]
        except KeyError:
            return default
        self.hash_table[self.find_index(key)] = []
        return value

    def update(
            self,
            iterable: Iterable | Dictionary = None,
            **kwargs
    ) -> None:

        if iterable:
            for key, value in iterable.items():
                self[key] = value
        else:
            for key, value in kwargs.items():
                self[key] = value

    def clear(self) -> None:
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]

    def find_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        for _ in range(self.capacity):
            print(index)
            if key in self.hash_table[index % self.capacity]:
                return index
            index = (index + 1) % self.capacity

        if hash(key) not in self.hash_table[index]:
            raise KeyError("Key does not exist")
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        threshold_coef = 0.625
        if len(self) >= self.capacity * threshold_coef:
            self.capacity *= 2
            tempo = Dictionary(self.items())
            self.hash_table = [[] for _ in range(self.capacity)]
            self.update(tempo)

        index = hash(key) % self.capacity
        if key in self.keys():
            del (self[key])

        while self.hash_table[index]:
            index = (index + 1) % self.capacity
        self.hash_table[index] = [key, value]

    def __getitem__(self, item: Hashable) -> Any:
        index = self.find_index(item)
        try:
            return self.hash_table[index][1]
        except IndexError:
            raise KeyError("Key does not exist")

    def __delitem__(self, key: Hashable) -> None:
        self.hash_table[self.find_index(key)] = []

    def __iter__(self) -> Iterator:
        return iter(value[1] for value in self.hash_table if value)

    def __len__(self) -> int:
        return len([1 for socket in self.hash_table if socket])

    def __str__(self) -> str:
        return "".join("{}: {}\n".format(
            socket[0], socket[1]) for socket in self.hash_table if socket
        )
