from __future__ import annotations
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.__capacity = 8
        self.__loadfactor = 2 / 3
        self.__size = 0
        self.__hash_table = [None] * self.__capacity
        self.__keys = []

    def __add_hash_node(self, key: Any, value: Any) -> None:
        hash_num = hash(key)
        slot = hash_num % self.__capacity
        while self.__hash_table[slot] is not None:
            slot = (slot + 1) % self.__capacity
        self.__hash_table[slot] = (key, hash_num, value)

    def __resize_hash_table(self) -> None:
        self.__hash_table += [None] * self.__capacity
        self.__capacity *= 2
        for index, hash_node in enumerate(self.__hash_table):
            if hash_node is not None:
                key, hash_num, value = hash_node
                self.__hash_table[index] = None
                self.__add_hash_node(key, value)

    @property
    def is_need_resize(self) -> bool:
        return self.__size > self.__capacity * self.__loadfactor

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_num = hash(key)
        try:
            self.__getitem__(key)
        except KeyError:
            self.__size += 1
            if self.is_need_resize:
                self.__resize_hash_table()
            self.__add_hash_node(key, value)
            self.__keys.append(key)
        old_value = self.__getitem__(key)
        node_index = self.__hash_table.index((key, hash_num, old_value))
        self.__hash_table[node_index] = (key, hash_num, value)

    def __getitem__(self, key: Any) -> Any:
        if key in self.__keys:
            hash_slot = hash(key) % self.__capacity
            node = self.__hash_table[hash_slot]
            if node is not None and node[0] == key:
                return node[2]
            for index, node in enumerate(self.__hash_table):
                if node is not None and node[0] == key:
                    return node[2]
        raise KeyError("Key is not in a dictionary")

    def __len__(self) -> int:
        return self.__size

    def __iter__(self) -> Dictionary:
        self.index = 0
        return self

    def __next__(self) -> Any:
        index = self.index
        if index >= len(self.__keys):
            raise StopIteration
        self.index += 1
        return self.__keys[index]

    def get(self, key: Any, value: Any = None) -> Any:
        try:
            dict_value = self.__getitem__(key)
        except KeyError:
            return value
        return dict_value

    def clear(self) -> None:
        self.__capacity = 8
        self.__size = 0
        self.__hash_table = [None] * self.__capacity
        self.__keys = []
