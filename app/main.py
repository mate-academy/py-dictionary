from dataclasses import dataclass
from typing import Any, Hashable, Iterable
from math import floor


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:
    default_capacity = 8
    load_factor = 2 / 3

    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list[Node | list | None] = [
            None
        ] * self.default_capacity
        self.capacity = self.default_capacity

    def __str__(self) -> str:
        return str(self.hash_table)

    def resize(self) -> None:
        elements = self.hash_table.copy()
        self.capacity = 2 * self.capacity
        self.hash_table = [None] * self.capacity
        self.length = 0
        for node in elements:
            if node:
                self.__setitem__(node.key, node.value)

    def calculate_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
            self.hash_table[index] is not None
            and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        threshold = floor(self.load_factor * self.capacity)
        if self.length >= threshold:
            self.resize()
        index = self.calculate_index(key)
        if self.hash_table[index] is None:
            self.length += 1
        self.hash_table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Any | KeyError:
        index = self.calculate_index(key)
        current_element = self.hash_table[index]
        if current_element is None:
            raise KeyError("No element with this key")
        return current_element.value

    def __len__(self) -> int:
        return self.length

    def items(self) -> list[tuple]:
        items = []
        for element in self.hash_table:
            if element:
                pair = (element.key, element.value)
                items.append(pair)
        return items

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        index = self.calculate_index(key)
        current_element = self.hash_table[index]
        if current_element:
            self.hash_table[index] = None
            self.length -= 1

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            value_to_return = self.__getitem__(key)
        except KeyError:
            return default
        else:
            return value_to_return

    def pop(self, key: Hashable, default: Any = None) -> Any:
        index = self.calculate_index(key)
        current_element = self.hash_table[index]
        if current_element is None and default is None:
            raise KeyError("No element with this key")
        if current_element is None and default:
            return default
        value_to_return = current_element.value
        self.hash_table[index] = None
        self.length -= 1
        return value_to_return

    def update(self, other: Iterable) -> None:
        if isinstance(other, Dictionary):
            for element in other.hash_table:
                if element:
                    self.__setitem__(element.key, element.value)
        else:
            for element in other:
                self.__setitem__(element[0], element[1])

    def __iter__(self) -> Hashable:
        for element in self.hash_table:
            if element:
                yield element.key
