from __future__ import annotations

from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.hash = hash(self.key)
        self.value = value

    def __repr__(self) -> str:
        return f"{self.key}: {self.value} (hash: {self.hash})"


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.fullness_of_table: int = 0
        self.load_factor: int = int(self.capacity * 2 / 3)
        self.hash_table: list = [None] * self.capacity

    def __repr__(self) -> str:
        result_str: str = ""
        for item in self.hash_table:
            if item is not None:
                result_str += f"{item.key}: {item.value} (hash: {item.hash})\n"
        return result_str[:-1]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        node: Node = Node(key, value)
        if self.fullness_of_table > self.load_factor:
            self.resize()
        self.input_node_in_hash_table(node)

    def __getitem__(self, key: Hashable) -> Any:
        no_cell: int = hash(key) % self.capacity
        find: bool = False
        for cell in range(no_cell, no_cell + self.capacity + 1):
            cell %= self.capacity
            if (isinstance(self.hash_table[cell], Node)
                    and self.hash_table[cell].key == key):
                find = True
                return self.hash_table[cell].value
        if not find:
            raise KeyError(f"{key} is not find!")

    def __len__(self) -> int:
        return self.fullness_of_table

    def __delitem__(self, key: Hashable) -> None:
        no_cell: int = key % self.capacity
        find: bool = False
        for cell in range(no_cell, no_cell + self.capacity + 1):
            cell %= self.capacity
            if (isinstance(self.hash_table[cell], Node)
                    and self.hash_table[cell].key == key):
                find = True
                self.hash_table[cell] = None
                self.fullness_of_table -= 1
                break
        if not find:
            raise KeyError(f"{key} is not find!")

    def __iter__(self) -> Dictionary:
        self.current = 0
        return self

    def __next__(self) -> Node | str:
        try:
            while self.hash_table[self.current] is None:
                self.current += 1
            next_value: int = self.hash_table[self.current]
            self.current += 1
            return next_value
        except IndexError:
            self.current = 0
            raise EOFError("End of file.")

    def clear(self) -> None:
        self.hash_table: list = [None] * self.capacity
        self.fullness_of_table = 0

    def get(self, key: Hashable, value: Any = None) -> Any | None:
        try:
            self.__getitem__(key)
        except KeyError:
            return value

    def pop(self, key: Hashable) -> Any | None:
        try:
            return_value: Any = self.__getitem__(key)
            self.__delitem__(key)
            return return_value
        except KeyError:
            return None

    def update(self, other: Dictionary | dict | list) -> Dictionary:
        if isinstance(other, Dictionary):
            for item in other.hash_table:
                if isinstance(item, Node):
                    self.__setitem__(item.key, item.value)
        if isinstance(other, dict):
            for key, value in other.items():
                self.__setitem__(key, value)
        if isinstance(other, list):
            for item in other:
                self.__setitem__(item[0], item[1])
        return self

    def input_node_in_hash_table(self, node: Node) -> None:
        no_cell: int = node.hash % self.capacity
        while (self.hash_table[no_cell] is not None
               and self.hash_table[no_cell].key != node.key):
            no_cell = (no_cell + 1) % self.capacity
        if self.hash_table[no_cell] is None:
            self.fullness_of_table += 1
        self.hash_table[no_cell] = node

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.load_factor: int = int(self.capacity * 2 / 3)
        self.clear()
        for cell in old_hash_table:
            if isinstance(cell, Node):
                self.input_node_in_hash_table(cell)
