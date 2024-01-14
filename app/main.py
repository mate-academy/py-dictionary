from __future__ import annotations

from typing import Any, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            value: Any,
            hash_key: int,
    ) -> None:
        self.key = key
        self.value = value
        self.hash_key = hash_key


class Dictionary:
    def __init__(self) -> None:
        self.length: int = 0
        self.hash_table: list = [None] * 8

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        if self.length == 0:
            return "{}"
        result = "{\n"

        for element in self.hash_table:
            if element:
                result += f'\t"{element.key}": {element.value}\n'
        result += "}"
        return result

    def resize_hash_table(self) -> list:
        hash_table_temporary = [None] * len(self.hash_table) * 2
        for element in self.hash_table:
            if element:
                new_index = hash(element.key) % len(hash_table_temporary)

                while hash_table_temporary[new_index]:
                    if new_index == len(hash_table_temporary) - 1:
                        new_index = 0
                    else:
                        new_index += 1

                hash_table_temporary[new_index] = element
        return hash_table_temporary

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        try:
            self.hash_table[self.calculate_hash_table_index(key)].value = value
        except KeyError:
            hash_table_index = hash(key) % len(self.hash_table)
            while self.hash_table[hash_table_index]:
                hash_table_index = ((hash_table_index + 1)
                                    % len(self.hash_table))

            self.hash_table[hash_table_index] = Node(key, value, hash(key))
            self.length += 1

        if self.length > len(self.hash_table) * 2 / 3:
            self.hash_table = self.resize_hash_table()

    def get(
            self,
            key: Hashable,
            default_value: Any = None
    ) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default_value

    def __getitem__(
            self,
            key: Hashable
    ) -> Any:
        return self.hash_table[self.calculate_hash_table_index(key)].value

    def __delitem__(
            self,
            key: Hashable
    ) -> None:
        self.hash_table[self.calculate_hash_table_index(key)] = None
        self.length -= 1

    def pop(
            self,
            key: Hashable,
            default_value: Any = None
    ) -> Any:

        try:
            pop_value = self.__getitem__(key)
        except KeyError:
            return default_value
        else:
            self.hash_table[self.calculate_hash_table_index(key)] = None
            self.length -= 1
            return pop_value

    def clear(self) -> None:
        self.hash_table.clear()
        self.length = 0

    def __iter__(self) -> Dictionary:
        self.current_element = 0
        return self

    def __next__(self) -> str:
        if self.current_element >= len(self.hash_table) - 1:
            raise StopIteration

        while not self.hash_table[self.current_element]:
            if self.current_element >= len(self.hash_table) - 1:
                raise StopIteration
            self.current_element += 1

        result = (f"\t'{self.hash_table[self.current_element].key}': "
                  f"{self.hash_table[self.current_element].value}\n")
        self.current_element += 1
        return result

    def calculate_hash_table_index(
            self,
            key: Hashable
    ) -> int:
        hash_table_index = hash(key) % len(self.hash_table)

        if (self.hash_table[hash_table_index]
                and self.hash_table[hash_table_index].key == key
                and self.hash_table[hash_table_index].hash_key == hash(key)):
            return hash_table_index
        index = 0
        while index < len(self.hash_table):
            if (self.hash_table[index]
                    and self.hash_table[index].key == key
                    and self.hash_table[index].hash_key == hash(key)):
                return index
            index += 1
        raise KeyError(f"No such key {key} in dictionary")
