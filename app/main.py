from __future__ import annotations
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length_dict = 0
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]
        self.filling = int(self.capacity * (2 / 3))

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length_dict > self.filling:
            self.resize()

        hash_key, index_key = self._index(key)

        while True:
            if not self.hash_table[index_key]:
                self.hash_table[index_key] = [key, hash_key, value]
                self.length_dict += 1
                break
            else:
                if (
                        key == self.hash_table[index_key][0]
                        and hash_key == self.hash_table[index_key][1]
                ):
                    self.hash_table[index_key][2] = value
                    break

            index_key = self._check_out_of_range(index_key)

    def __getitem__(self, key: Any) -> list:
        hash_key, index_key = self._index(key)
        count_check = 0

        while True:
            if self.hash_table[index_key]:
                if (
                        self.hash_table[index_key][0] == key
                        and self.hash_table[index_key][1] == hash_key
                ):
                    return self.hash_table[index_key][2]

            index_key = self._check_out_of_range(index_key)
            count_check += 1

            if count_check >= len(self.hash_table):
                raise KeyError

    def __len__(self) -> int:
        return self.length_dict

    def __iter__(self) -> Dictionary:
        self.it = 0
        return self

    def __next__(self) -> Any:
        while True:
            if self.it >= len(self.hash_table):
                raise StopIteration
            if self.hash_table[self.it]:
                key = self.hash_table[self.it][0]
                self.it += 1

                return key

            self.it += 1

    def __delitem__(self, key: Any) -> None:
        hash_key, index_key = self._index(key)
        count_check = 0

        while True:
            if self.hash_table[index_key]:
                if (
                        self.hash_table[index_key][0] == key
                        and self.hash_table[index_key][1] == hash_key
                ):
                    self.hash_table[index_key] = []
                    self.length_dict -= 1
                    break

            index_key = self._check_out_of_range(index_key)
            count_check += 1

            if count_check >= len(self.hash_table):
                raise KeyError

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self.capacity)]
        self.length_dict = 0

    def get(self, key: Any) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None

    def pop(self, key: Any) -> Any:
        try:
            pop_value = self.__getitem__(key)
            self.__delitem__(key)

            return pop_value
        except KeyError:
            raise KeyError

    def update(self, other_dict: Dictionary) -> None:
        for other_item in other_dict.hash_table:
            if other_item:
                self.__setitem__(other_item[0], other_item[2])

    def resize(self) -> None:
        self.capacity *= 2
        self.filling = int(self.capacity * (2 / 3))
        old_hash_table = self.hash_table
        self.clear()

        for item in old_hash_table:
            if item:
                self.__setitem__(item[0], item[2])

    def _index(self, key: Any) -> tuple[int, int]:
        hash_key = hash(key)
        index_key = hash_key % self.capacity

        return hash_key, index_key

    def _check_out_of_range(self, index: int) -> int:
        if index < len(self.hash_table) - 1:
            index += 1
        else:
            index = 0

        return index
