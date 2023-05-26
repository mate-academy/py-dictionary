from __future__ import annotations
from typing import List, Any, Hashable
import traceback


class Dictionary:
    def __init__(self) -> None:
        self.load_factor = 2 / 3
        self.length = 0
        self.capacity = 8
        self.hash_table: List = [None] * self.capacity

    def __str__(self) -> str:
        return str(self.hash_table)

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Dictionary:
        self.current_element = 0
        return self

    def __next__(self) -> Hashable:
        while self.hash_table[self.current_element] is None:
            self.current_element += 1
            if self.current_element > self.capacity - 1:
                raise StopIteration
        result = self.hash_table[self.current_element]
        self.current_element += 1
        return result

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if self.length >= round(self.capacity * self.load_factor):
            self.resize()
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while self.hash_table[index] is not None:
            current_key, current_value, hash_of_key = self.hash_table[index]
            if current_key == key and hash_of_key == hashed_key:
                self.hash_table[index] = [current_key, value, hashed_key]
                return
            index = (index + 1) % self.capacity
        self.hash_table[index] = [key, value, hashed_key]
        self.length += 1

    def __getitem__(
            self,
            item: Hashable
    ) -> Any:
        hashed_item = hash(item)
        index = hashed_item % self.capacity
        while self.hash_table[index] is not None:
            key, value, hash_of_key = self.hash_table[index]
            if key == item and hash_of_key == hashed_item:
                return value
            index = (index + 1) % self.capacity
        raise KeyError(f"Incorrect key {item}")

    def __delitem__(
            self,
            key: Hashable
    ) -> None:
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while self.hash_table[index] is not None:
            current_key, current_value, hash_of_key = self.hash_table[index]
            if current_key == key and hash_of_key == hashed_key:
                self.hash_table[index] = ["dummy", 0, "fake_hash"]
                self.length -= 1
                return
            index = (index + 1) % self.capacity
        raise KeyError(f"Incorrect key {key}")

    def resize(self) -> None:
        self.length = 0
        self.capacity *= 2
        temporary_list = self.hash_table
        self.hash_table = [None] * self.capacity
        for item in temporary_list:
            if item is not None:
                key, value, hash_of_key = item
                self.__setitem__(key, value)

    def clear(self) -> None:
        self.__init__()

    def get(
            self,
            key: Hashable
    ) -> Any:
        return self.__getitem__(key)

    def pop(
            self,
            key: Hashable
    ) -> Any:
        try:
            self.length -= 1
            return [self.get(key), self.__delitem__(key)][0]
        except KeyError:
            traceback.print_exc()

    def update(self, dictionary: Dictionary) -> None:
        for item in dictionary.hash_table:
            if item is not None:
                key, value, hash_of_key = item
                self.__setitem__(key, value)
