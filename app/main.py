import copy
from typing import Any, Hashable, Union, Iterable


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return f"{self.key} : {self.value}"


class Dictionary:
    LOAD_FACTOR = 0.75
    INITIAL_LENGTH = 8

    def __init__(self) -> None:
        self.length: int = 0
        self.hash_table_length: int = self.INITIAL_LENGTH
        self.hash_table: list[Union[Node, None]] = [None] * self.INITIAL_LENGTH

    def __len__(self) -> int:
        return self.length

    def hash_index(self, key: Hashable, next_index: int = 0) -> int:
        if next_index:
            return (hash(key) + next_index) % len(self.hash_table)
        return hash(key) % len(self.hash_table)

    def set_node(self, key: Hashable, value: Any) -> None:
        index = self.hash_index(key)
        count = 0
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = Node(key, value)
                self.length += 1
                break
            elif self.hash_table[index].key == key:
                self.hash_table[index].value = value
                break
            count += 1
            index = self.hash_index(key, count)

    def extend_hash_table(self) -> None:
        self.hash_table_length *= 2
        old_hash_table = copy.deepcopy(self.hash_table)
        self.hash_table = [None] * self.hash_table_length
        self.length = 0
        for node in old_hash_table:
            if node:
                self.set_node(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length + 1 >= len(self.hash_table) * self.LOAD_FACTOR:
            self.extend_hash_table()
        self.set_node(key, value)

    def __getitem__(self, key: Hashable, return_index: bool = False) -> Any:
        index = self.hash_index(key)
        count = 0
        for _ in range(len(self.hash_table)):
            if self.hash_table[index] and self.hash_table[index].key == key:
                if return_index:
                    return index
                return self.hash_table[index].value
            count += 1
            index = self.hash_index(key, count)
        raise KeyError(f"Item with key {key} does not exist!!!")

    def __delitem__(self, key: Hashable) -> None:
        self.hash_table[self.__getitem__(key, return_index=True)] = None

    def clear(self) -> None:
        self.hash_table = [None] * self.INITIAL_LENGTH

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            self.__getitem__(key)
        except KeyError:
            return default_value

    def pop(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            self.__getitem__(key)
            self.__delitem__(key)
        except KeyError:
            if default_value is not None:
                return default_value
            raise KeyError("Default value must be set if key not found")

    def update(self, other: Iterable = None) -> None:
        if isinstance(other, dict):
            for key, value in other.items():
                self.__setitem__(key, value)
        if isinstance(other, (tuple, list, set)):
            for key, value in other:
                self.__setitem__(key, value)

    def __iter__(self) -> Any:
        self.position = 0
        return self

    def __next__(self) -> list:
        if self.position < len(self.hash_table):
            if self.hash_table[self.position] is None:
                while self.hash_table[self.position] is None:
                    self.position += 1
                    if self.position == len(self.hash_table):
                        raise StopIteration
            out = [self.hash_table[self.position].key,
                   self.hash_table[self.position].value]
            self.position += 1
            return out

        raise StopIteration
