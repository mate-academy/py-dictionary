from typing import Any, Optional, Iterator
from dataclasses import dataclass


class Dictionary:

    @dataclass
    class Node:
        key: Any
        hash_value: int
        value: Any

    initial_capacity = 8
    load_factor = 2 / 3

    def __init__(self) -> None:
        self.__storage: list[Optional[Dictionary.Node]] = (
            [None] * Dictionary.initial_capacity
        )
        self.__capacity = Dictionary.initial_capacity
        self.__len = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.__len >= int(self.__capacity * Dictionary.load_factor):
            self.__resize()

        h_code = hash(key)
        index = h_code % self.__capacity

        while self.__storage[index] is not None:
            if self.__storage[index].key == key:
                self.__storage[index].value = value
                break
            index = (index + 1) % self.__capacity
        else:
            self.__storage[index] = Dictionary.Node(key, h_code, value)
            self.__len += 1

    def __resize(self) -> None:
        if self.__len < int(self.__capacity * Dictionary.load_factor):
            return

        old_storage = self.__storage
        self.__capacity *= 2
        self.__storage = [None] * self.__capacity

        for node in old_storage:
            if node is not None:
                index = node.hash_value % self.__capacity
                while self.__storage[index] is not None:
                    index = (index + 1) % self.__capacity
                self.__storage[index] = node

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.__capacity
        start_index = index

        while self.__storage[index] is not None:
            if self.__storage[index].key == key:
                return self.__storage[index].value
            index = (index + 1) % self.__capacity
            if start_index == index:
                break

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.__len

    def clear(self) -> None:
        self.__storage = [None] * self.__capacity
        self.__len = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __iter__(self) -> Iterator[Any]:
        return (node.key for node in self.__storage if node is not None)
