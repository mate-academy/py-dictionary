from typing import Any, Union

import copy

HashableSequence = Union[int, float, str, object, tuple]


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table = [None] * 8

    def resize(self) -> None:
        if self.__len__() + 1 >= 2 / 3 * len(self.hash_table):
            old_hash_table = copy.copy(self.hash_table)
            self.hash_table = [None] * len(self.hash_table) * 2
            for item in old_hash_table:
                if item:
                    self.__setitem__(item[0], item[2])
                    self.length -= 1

    def __getitem__(self, key: HashableSequence) -> Any:
        index = int(self.__hash__(key) % len(self.hash_table))
        for i in range(len(self.hash_table)):
            if self.hash_table[index] and self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index += 1
            if index == len(self.hash_table):
                index = 0
        raise KeyError

    def __setitem__(self, key: HashableSequence, value: Any) -> None:
        self.resize()
        hashed_key = self.__hash__(key)
        index = hashed_key % len(self.hash_table)
        if self.hash_table[index]:
            for i in range(len(self.hash_table)):
                if self.hash_table[index][0] == key:
                    self.hash_table[index] = (key, hashed_key, value)
                    break
                index += 1
                if index == len(self.hash_table):
                    index = 0
                if not self.hash_table[index]:
                    self.hash_table[index] = (key, hashed_key, value)
                    self.length += 1
                    break
        else:
            self.hash_table[index] = (key, hashed_key, value)
            self.length += 1

    def __len__(self) -> int:
        return self.length

    def __hash__(self, key: HashableSequence) -> int:
        if isinstance(key, str):
            return sum(ord(char) for char in key)
        return hash(key)

    def clear(self) -> None:
        self.length = 0
        self.hash_table = [None] * 8

    def __delitem__(self, key: HashableSequence) -> None:
        self.hash_table[self.__hash__(key) % len(self.hash_table)] = None
        self.length -= 1

    def get(self, key: HashableSequence) -> Any:
        return self.__getitem__(key)

    def pop(self, key: HashableSequence) -> tuple:
        item = self.hash_table[self.__hash__(key) % len(self.hash_table)]
        self.hash_table[self.__hash__(key) % len(self.hash_table)] = None
        self.length -= 1
        return item

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self.__setitem__(key, value)

    def __iter__(self) -> list:
        return self.hash_table
