from __future__ import annotations
from typing import Any, Hashable


EMPTY = object()


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.__hash_table = [Node() for _ in range(0, self.capacity)]

    def max_size(self) -> int:
        return round(self.capacity * 2 / 3)

    def extend_hash_table_capacity(self) -> None:
        old_table = self.__hash_table.copy()
        self.__hash_table = [Node() for _ in range(self.capacity * 2)]
        self.capacity = len(self.__hash_table)
        for elem in old_table:
            if elem.hash:
                index = hash(elem.key) % self.capacity
                while self.__hash_table[index].hash:
                    index = (index + 1) % self.capacity
                self.__hash_table[index].key = elem.key
                self.__hash_table[index].hash = elem.hash
                self.__hash_table[index].value = elem.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity
        if (self.__hash_table[index].hash == hash(key)
                and self.__hash_table[index].key == key):
            self.__hash_table[index].value = value
            return
        else:
            index = self.search_for_index(index, key)
            if index is not None:
                self.__hash_table[index].value = value
                return
        self.extend_size()
        index = hash(key) % self.capacity
        while self.__hash_table[index].hash:
            index = (index + 1) % len(self.__hash_table)
        self.__hash_table[index].hash = hash(key)
        self.__hash_table[index].key = key
        self.__hash_table[index].value = value
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        return self.__hash_table[index].value

    def __len__(self) -> int:
        return self.size

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        if (self.__hash_table[index].hash != hash(key)
                or self.__hash_table[index].key != key):
            index = self.search_for_index(index, key)
            if index is None:
                raise KeyError
        return index

    def search_for_index(self, index: int, key: Hashable) -> None | int:
        new_index = (index + 1) % self.capacity
        while new_index != index:
            if (self.__hash_table[new_index].hash == hash(key)
                    and self.__hash_table[new_index].key == key):
                return new_index
            new_index = (new_index + 1) % self.capacity
        return None

    def extend_size(self) -> None:
        if self.size == self.max_size():
            self.extend_hash_table_capacity()

    def clear(self) -> None:
        for elem in self.__hash_table:
            self.clear_node(elem)
        self.size = 0

    def clear_node(self, node: Node) -> None:
        node.hash = None
        node.key = EMPTY
        node.value = EMPTY

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)
        self.clear_node(self.__hash_table[index])
        self.size -= 1

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
        except KeyError:
            return default
        else:
            return value

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            index = self.get_index(key)
        except KeyError:
            return default
        else:
            my_value = self.__hash_table[index].value
            self.clear_node(self.__hash_table[index])
            self.size -= 1
            return my_value

    def update(self, insert_dict: Dictionary) -> None:
        for elem in insert_dict:
            self.__setitem__(elem.key, elem.value)

    def __iter__(self) -> iter:
        for element in self.__hash_table:
            if element.key != EMPTY:
                yield element.key


class Node:
    def __init__(self) -> None:
        self.key = EMPTY
        self.hash = None
        self.value = EMPTY
