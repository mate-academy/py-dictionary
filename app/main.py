from typing import Hashable, Any, Optional, Iterable


class Dictionary:

    def __init__(self) -> None:
        self._capacity = 8
        self._load_factor = 0.67
        self._length = 0
        self._hash_table: list = [None] * self._capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._length > self._capacity * self._load_factor:
            self._increase_capacity()

        index = self._find_index(key)
        if not self._hash_table[index]:
            self._length += 1
        self._hash_table[index] = key, hash(key), value

    def _increase_capacity(self) -> None:
        table_to_resize = self._hash_table
        self._capacity *= 2
        self._hash_table = [None] * self._capacity
        self._length = 0

        for cell in table_to_resize:
            if cell:
                self.__setitem__(cell[0], cell[2])

    def _find_index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity
        while self._hash_table[index] and self._hash_table[index][0] != key:
            index += 1
            index %= self._capacity
        return index

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key)
        if not self._hash_table[index]:
            raise KeyError(f"Key {key} is not in dictionary")
        return self._hash_table[index][2]

    def __len__(self) -> int:
        return self._length

    def clear(self) -> None:
        self._hash_table = [None] * self._capacity
        self._length = 0

    def __delitem__(self, key: Hashable) -> None:
        index = self._find_index(key)
        if self._hash_table[index]:
            self._hash_table[index] = [None]
            self._length -= 1

    def get(self, key: Hashable) -> Any:
        return self.__getitem__(key)

    def pop(
            self,
            key: Hashable,
            default_value: Optional[Any]
    ) -> Any:

        index = self._find_index(key)
        if self._hash_table[index][0] != key and not default_value:
            raise KeyError(f"Key {key} is not in dictionary")
        pop_item = self._hash_table[index] or default_value
        self._hash_table[index] = None
        self._length -= 1
        return pop_item

    def update(self, iterable: Iterable) -> None:
        for key, value in enumerate(iterable):
            index = self._find_index(key)
            if self._hash_table[index]:
                self._hash_table[index][2] = value
                continue
            self._hash_table[index] = key, hash(key), value
            self._length += 1

    def __iter__(self) -> Iterable:
        return iter(self._hash_table)
