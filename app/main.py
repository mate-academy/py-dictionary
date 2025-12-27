from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    index: int
    value: Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = self.capacity / 3 * 2
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        index = self.__get_index(key)
        if not self.table[index]:
            self.table[index] = Node(key, index, value)
            self.size += 1
        else:
            existing_node = self.table[index]
            while existing_node:
                if existing_node.key == key:
                    existing_node.value = value
                    return
                index += 1
                index %= self.capacity
                existing_node = self.table[index]
            self.table[index] = Node(key, index, value)
            self.size += 1
        if self.size >= self.load_factor:
            self.__resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__get_index(key)
        existing_node = self.table[index]
        while existing_node:
            if existing_node.key == key:
                return existing_node.value
            index += 1
            index %= self.capacity
            existing_node = self.table[index]
        raise KeyError(f"There is no key: {key}")

    def __len__(self) -> int:
        return self.size

    def __resize(self) -> None:
        self.capacity *= 2
        self.load_factor = self.capacity / 3 * 2
        previous_table = self.table
        self.table = [None] * self.capacity
        for node in previous_table:
            if node:
                index = self.__get_index(node.key)
                while self.table[index]:
                    index += 1
                    index %= self.capacity
                self.table[index] = node

    def __get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def clear(self) -> None:
        self.capacity = 8
        self.load_factor = self.capacity / 3 * 2
        self.size = 0
        self.table = [None] * self.capacity

    def get(self, key: Hashable) -> Any:
        try:
            return self[key]
        except KeyError as e:
            return e

    def pop(self, key: Hashable, default: Any = None) -> Any:
        if key in self:
            result = self[key]
            del self[key]
            return result
        if default:
            return default
        raise KeyError

    def update(
            self,
            other: [
                "Dictionary",
                dict,
                tuple,
                set,
                list
            ] = None
    ) -> None:
        if not other:
            return
        if isinstance(other, dict):
            other = other.items()
        key, value = other
        self[key] = value

    def __iter__(self) -> Hashable:
        for node in self.table:
            while node:
                yield node.key
                node = node.next
