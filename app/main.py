from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._table = [None] * self._capacity
        self._size = 0
        self._load_factor = 2 / 3

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: int, value: Any) -> None:
        if self._size >= self._capacity * self._load_factor:
            self._resize()
        self._add_item_to_table(key, value)

    def __getitem__(self, key: int) -> None:
        index = self._find_index(key)

        if self._table[index] is None:
            raise KeyError(f"There is no key: '{key}'")

        return self._table[index][2]

    def _add_item_to_table(self, key: int, value: Any) -> None:
        index = self._find_index(key)

        if self._table[index] is None:
            self._size += 1

        self._table[index] = (hash(key), key, value)

    def _find_index(self, key: int) -> int:
        hash_code = hash(key)
        index = hash_code % self._capacity

        while (self._table[index] is not None
               and (self._table[index][0] != hash_code
                    or self._table[index][1] != key)):
            index += 1
            index %= self._capacity

        return index

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0

        for item in old_table:
            if item is not None:
                self.__setitem__(item[1], item[2])
