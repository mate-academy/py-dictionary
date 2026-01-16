from __future__ import annotations
from typing import Any, Hashable
from copy import copy


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.__capacity = 8
        self.__hash_table = [None for _ in range(self.__capacity)]

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        result = ""
        for item in self.__hash_table:
            if item:
                result += f"{item[0]}: {item[2]}, "
        return f"{{{result}}}"

    def __iter__(self) -> Dictionary:
        self.__iteration_index = 0
        return self

    def __next__(self) -> Any:

        while True:
            self.__iteration_index += 1
            if self.__iteration_index > self.__capacity:
                raise StopIteration
            if self.__hash_table[self.__iteration_index - 1]:
                return self.__hash_table[self.__iteration_index - 1][0]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.length += 1
        if self.length > (2 / 3 * self.__capacity):
            self.__resize()

        self.__set_item_in_hash_table(key, value, self.__hash_table)

    def __getitem__(self, key: Hashable) -> Any:
        hash_index = self.__get_hash_index(key)
        hash_index = self.__find_index(key, hash_index)
        return self.__hash_table[hash_index][2]

    def __delitem__(self, key: Hashable) -> None:
        hash_index = self.__get_hash_index(key)
        hash_index = self.__find_index(key, hash_index)
        self.length -= 1
        self.__hash_table[hash_index] = None

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def clear(self) -> None:
        self.__init__()

    def update(self, new_dict: Dictionary) -> None:
        for key in new_dict:
            self[key] = new_dict[key]

    def pop(self, key: Hashable) -> Any:
        element = self[key]
        del self[key]
        return element

    def __find_index(self, key: Hashable, hash_index: int) -> int:
        key_found = False
        for _ in range(self.__capacity):
            if self.__hash_table[hash_index] is None:
                hash_index = (hash_index + 1) % self.__capacity
                continue
            key_hash = hash(key)
            element_hash = hash(self.__hash_table[hash_index][0])
            if (key == self.__hash_table[hash_index][0]
                    and key_hash == element_hash):
                key_found = True
                break
            hash_index = (hash_index + 1) % self.__capacity

        if not key_found:
            raise KeyError(f"Key {key} does not exist")

        return hash_index

    def __get_hash_index(self, key: Hashable) -> int:
        hash_key = hash(key)
        hash_index = hash_key % self.__capacity
        return hash_index

    def __set_item_in_hash_table(
            self, key: Hashable, value: Any, hash_table: list[Any]
    ) -> None:
        hash_key = hash(key)
        hash_index = self.__get_hash_index(key)

        while True:
            if (hash_table[hash_index] is None
                    or hash_table[hash_index][0] == key):
                if hash_table[hash_index] is not None:
                    self.length -= 1
                hash_table[hash_index] = [key, hash_key, value]
                break

            hash_index = (hash_index + 1) % self.__capacity

    def __resize(self) -> None:
        self.__capacity *= 2
        new_hash_table = [None for _ in range(self.__capacity)]

        for item in self.__hash_table:
            if item is None:
                continue
            self.__set_item_in_hash_table(item[0], item[2], new_hash_table)

        self.__hash_table = copy(new_hash_table)
