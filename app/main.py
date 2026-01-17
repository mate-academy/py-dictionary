from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Any, Iterator, Iterable, Optional, Union


class Dictionary:
    @dataclass
    class Node:
        key: Hashable
        value: Any
        hash_: int

    def __init__(self) -> None:
        self.__capacity = 8
        self.__threshold = Fraction(2, 3)
        self.__table = [None] * self.__capacity
        self.__length = 0
        self.__deleted = object()

    def __find_index(self, key: Hashable) -> int:
        index = hash(key) % self.__capacity
        while True:
            if not self.__table[index]:
                return -1
            if (self.__table[index] != self.__deleted
                    and key == self.__table[index].key):
                return index
            index = (index + 1) % self.__capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.__length + 1 > round(self.__capacity * self.__threshold):
            self.__double_capacity()

        node = self.Node(key, value, hash(key))
        index = self.__find_index(key)

        if index == -1:
            index = hash(key) % self.__capacity
            while (self.__table[index] is not None
                   and self.__table[index] != self.__deleted):
                index = (index + 1) % self.__capacity
            self.__length += 1

        self.__table[index] = node

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__find_index(key)
        if index == -1:
            raise KeyError(f"no such key: {key}")
        return self.__table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self.__find_index(key)
        if index == -1:
            raise KeyError(f"no such key: {key}")
        self.__table[index] = self.__deleted
        self.__length -= 1

    def __len__(self) -> int:
        return self.__length

    def __iter__(self) -> Iterator:
        for node in self.__table:
            if node and node != self.__deleted:
                yield node.key, node.value

    def pop(self, key: Hashable, default: Optional[Any] = None) -> Any:
        index = self.__find_index(key)
        if index == -1:
            if default is None:
                raise KeyError(f"no such key: {key}")
            return default
        value = self.__table[index].value
        self.__table[index] = self.__deleted
        self.__length -= 1
        return value

    def __double_capacity(self) -> None:
        old_table = self.__table
        self.__capacity *= 2
        self.__table = [None] * self.__capacity
        self.__length = 0

        for node in old_table:
            if node and node != self.__deleted:
                self[node.key] = node.value

    def items(self) -> list[tuple[Hashable, Any]]:
        return [
            (node.key, node.value) for node in self.__table
            if node and node != self.__deleted
        ]

    def update(
        self,
        source: Union[
            dict, "Dictionary", Iterable[tuple[Hashable, Any]]
        ] = None,
        **kwargs
    ) -> None:
        if source:
            if isinstance(source, (dict, Dictionary)):
                source = source.items()
            for key, value in source:
                self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def clear(self) -> None:
        self.__init__()
