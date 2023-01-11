import copy
from typing import Any, Union

from app.point import Point


class Dictionary:

    def __init__(self) -> None:
        self.size = 0
        self.hash_table = [[None]] * 8

    def resize(self) -> list:
        old_hash_table = copy.deepcopy(self.hash_table)
        capacity = len(old_hash_table) * 2
        self.hash_table = [[None]] * capacity
        self.size = 0
        for key_value_pair in old_hash_table:
            if key_value_pair[0] is not None:
                self.__setitem__(key_value_pair[0], key_value_pair[1])
        return self.hash_table

    def __setitem__(
            self,
            key: Union[str, int, tuple, Point],
            value: Any
    ) -> list:
        fill_factor = 0.625
        if self.size / len(self.hash_table) >= fill_factor:
            self.hash_table = self.resize()
        index = hash(key) % len(self.hash_table)
        if self.hash_table[index][0] is None:
            self.hash_table[index] = [key, value]
            self.size += 1
        self.hash_table = self.handle_existing_key(key, value)
        return self.hash_table

    def handle_existing_key(
            self,
            key: Union[str, int, tuple, Point],
            value: Any
    ) -> list:
        index = hash(key) % len(self.hash_table)
        for key_value_list in self.hash_table:
            if key_value_list[0] == key:
                key_value_list[1] = value
                return self.hash_table
        next_index = (index + 1) % len(self.hash_table)
        while self.hash_table[next_index][0] is not None:
            next_index = (next_index + 1) % len(self.hash_table)
        self.hash_table[next_index] = [key, value]
        self.size += 1
        return self.hash_table

    def __getitem__(self, input_key: Union[str, int, tuple, Point]) -> Any:
        for key in self.hash_table:
            if key[0] == input_key:
                return key[1]
        raise KeyError(f"Key {input_key} does not exist")

    def __len__(self) -> int:
        return self.size

    def __delitem__(self, key: Union[str, int, tuple, Point]) -> None:
        if self.size / len(self.hash_table) >= 0.75:
            self.hash_table = self.resize()
        index = hash(key) % len(self.hash_table)
        del self.hash_table[index]
        self.hash_table.insert(index, [None])

    def clear(self) -> list:
        self.hash_table.clear()
        self.size = 0
        self.hash_table = [(None,)] * 8
        return self.hash_table

    def pop(self, key: Union[str, int, tuple, Point]) -> Any:
        index = hash(key) % len(self.hash_table)
        del_element = self.hash_table.pop(index)
        self.hash_table.insert(index, [None])
        return del_element
