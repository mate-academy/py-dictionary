from __future__ import annotations
from typing import List, Tuple, Any, Optional, Hashable
from dataclasses import dataclass


@dataclass
class Node:
    __slots__ = ("key", "hash_value", "value")

    key: Hashable
    hash_value: int
    value: Any

    def __repr__(self) -> str:
        return f"<Node: key={self.key} value={self.value}>"


class Dictionary:
    __LOAD_FACTOR: float = 3 / 2
    __capacity: int = 8
    __threshold: int = round(__capacity / __LOAD_FACTOR)

    def __init__(self) -> None:
        self.__items: List[Optional[Node]] = [None] * self.__capacity
        self.__size = 0

    def __get_hash_index(self, key: Hashable) -> int:
        try:
            hash_key = hash(key)
        except TypeError:
            raise KeyError(f"Unhashable key type: {type(key)}")

        hash_index = hash_key % self.__capacity

        while self.__items[hash_index] and self.__items[hash_index].key != key:
            hash_index = (hash_index + 1) % self.__capacity

        return hash_index

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_index = self.__get_hash_index(key)

        if self.__items[hash_index] and self.__items[hash_index].key == key:
            self.__items[hash_index].value = value
        else:
            self.__items[hash_index] = Node(key, hash(key), value)
            self.__size += 1

        if self.__size >= self.__threshold:
            self.__resize(self.__capacity * 2)

    def __getitem__(self, key: Any) -> Optional[Any]:
        hash_index = self.__get_hash_index(key)

        if self.__items[hash_index] and self.__items[hash_index].key == key:
            return self.__items[hash_index].value

        raise KeyError(f"Key {key} not exists")

    def __len__(self) -> int:
        return self.__size

    def __resize(self, new_size: int) -> None:
        self.__capacity = new_size
        self.__threshold = round(self.__capacity / self.__LOAD_FACTOR)
        self.__size = 0

        old_item_list = [item for item in self.__items if item]
        self.__items = [None] * self.__capacity

        for item in old_item_list:
            self[item.key] = item.value

    def clear(self) -> None:
        self.__capacity = 8
        self.__threshold = round(self.__capacity / self.__LOAD_FACTOR)
        self.__size = 0
        self.__items = [None] * self.__capacity

    def __delitem__(self, key: Hashable) -> None:
        hash_key = self.__get_hash_index(key)

        if self.__items[hash_key] and self.__items[hash_key].key == key:
            self.__items[hash_key] = None
            self.__size -= 1
            return

        raise KeyError(f"Key {key} not exists")

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        value = self.get(key)
        if not value:
            return default
        self.__delitem__(key)
        return value

    def update(self, other: Dictionary) -> None:
        for item in other:
            key, value = item
            self[key] = value

    def __iter__(self) -> Dictionary:
        self.__curr_position = 0
        return self

    def __next__(self) -> Tuple[Hashable, Any]:
        while (
            self.__curr_position < self.__capacity
            and not self.__items[self.__curr_position]
        ):
            self.__curr_position += 1

        if self.__curr_position >= self.__capacity:
            raise StopIteration

        curr_item = self.__items[self.__curr_position]
        self.__curr_position += 1

        return curr_item.key, curr_item.value
