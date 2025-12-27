from math import floor
from typing import Any, Iterable, Hashable


class Dictionary:
    def __init__(self) -> None:
        self._initial_capacity: int = 8
        self._load_factor: float = 2 / 3
        self._resize: int = 5
        self._length = 0
        self._hash_table: list = [None] * self._initial_capacity

    def _find_hash_index(self, key_item: Hashable) -> int:
        hash_index = hash(key_item) % self._initial_capacity
        cell_in_table = self._hash_table

        while cell_in_table[hash_index] is not None:
            if cell_in_table[hash_index][0] == key_item:
                break
            if hash_index < self._initial_capacity - 1:
                hash_index += 1
            else:
                hash_index = 0
        return hash_index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._resize <= self._length:
            self._initial_capacity *= 2
            self._resize = floor(self._initial_capacity * self._load_factor)

            temporary_hash_table = list(self._hash_table)
            self._hash_table = [None] * self._initial_capacity

            for cell_in_table in temporary_hash_table:
                if cell_in_table:
                    hash_index = self._find_hash_index(cell_in_table[0])
                    self._hash_table[hash_index] = [*cell_in_table]
            del temporary_hash_table

        hash_index = self._find_hash_index(key)
        self._hash_table[hash_index] = [key, hash(key), value]
        self._length = self._initial_capacity - self._hash_table.count(None)

    def __getitem__(self, item: Hashable) -> Any:
        hash_index = hash(item) % self._initial_capacity

        while self._hash_table[hash_index] is not None:
            if self._hash_table[hash_index][0] != item:
                if hash_index < self._initial_capacity - 1:
                    hash_index += 1
                else:
                    hash_index = 0
            else:
                return self._hash_table[hash_index][2]
        raise KeyError(f"Key {item} not in the hash table") from None

    def __delitem__(self, key: Hashable) -> None:
        hash_index = self._find_hash_index(key)
        self._hash_table[hash_index] = None
        self._length -= 1

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            result = self.__getitem__(key)
        except KeyError as error:
            if not default:
                raise error
            return default
        else:
            self.__delitem__(key)
            return result

    def update(self, iterable: Iterable) -> None:
        if isinstance(iterable, Dictionary):
            for item in iterable._hash_table:
                if item is not None:
                    self.__setitem__(item[0], item[2])
        elif isinstance(iterable, (list, tuple)):
            for item in iterable:
                self.__setitem__(item[0], item[1])
        else:
            raise TypeError(f"Unsupported type for {iterable}. "
                            f"Expected Dictionary, list, or tuple.")

    def __iter__(self) -> Iterable:
        return iter(
            [value[0] for value in self._hash_table if value is not None]
        )

    def items(self) -> Any:
        for item in self._hash_table:
            if item is not None:
                yield item[0], item[2]

    def __len__(self) -> int:
        return self._length
