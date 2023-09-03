from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._factor = 2 / 3
        self._size = 0
        self._hash_table = [None] * self._capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._size >= self._capacity * self._factor:
            self._resize()

        index = self._find_index(key)

        if self._hash_table[index] is None:
            self._size += 1
        self._hash_table[index] = (hash(key), key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key)

        if self._hash_table[index] is None:
            raise KeyError(key)

        return self._hash_table[index][2]

    def __len__(self) -> int:
        return self._size

    def _find_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash(key) % self._capacity

        while (
                self._hash_table[index] is not None
                and (
                self._hash_table[index][0] != hash_
                or self._hash_table[index][1] != key)
        ):
            index = (index + 1) % self._capacity

        return index

    def _resize(self) -> None:
        self._capacity *= 2
        old_hash_table = self._hash_table
        self._hash_table = [None] * self._capacity
        self._size = 0
        for item in old_hash_table:
            if item is not None:
                self.__setitem__(item[1], item[2])
