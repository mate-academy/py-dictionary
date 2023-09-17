from __future__ import annotations
from typing import Any, Iterable, Optional, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list[tuple | str | None] = [None] * 8
        self._doom_value = "Some doom value"

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key)

        if self.length + 1 > len(self.hash_table) * 2 / 3:
            self._resize()

        index = hash_value % len(self.hash_table)

        while (self.hash_table[index] is not None
               and self.hash_table[index] != self._doom_value):
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, value)
                return
            index = (index + 1) % len(self.hash_table)

        self.hash_table[index] = (key, value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index = hash_value % len(self.hash_table)

        while self.hash_table[index] is not None:
            hashed_key, value = self.hash_table[index]
            if hashed_key == key:
                return value
            index = (index + 1) % len(self.hash_table)

        raise KeyError

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        self.length = 0
        elements = [element for element in self.hash_table
                    if element != self._doom_value and element is not None]
        self.hash_table = [None] * len(self.hash_table) * 2
        for key, value in elements:
            self.__setitem__(key, value)

    def clear(self) -> None:
        self.hash_table = [None] * len(self.hash_table)

    def __delitem__(self, key: Hashable) -> None:
        try:
            hash_value = hash(key)
            index = hash_value % len(self.hash_table)
            value = self.hash_table[index]

            if value is None:
                raise KeyError

            self.hash_table[index] = self._doom_value
            self.length -= 1
        except TypeError:
            raise

    def pop(self, key: Hashable, default_value: Optional[Any] = None) -> Any:
        value = self.get(key)

        if value is None:
            return default_value

        self.__delitem__(key)
        return value

    def get(self, key: Hashable, default_value: Optional[Any] = None) -> Any:
        try:
            self.__getitem__(key)
        except KeyError:
            return default_value

    def __iter__(self) -> Iterable[Hashable]:
        return [element[0] for element in self.hash_table
                if element != self._doom_value and element is not None]

    def items(self) -> Iterable[tuple[Hashable, Any]]:
        return [element for element in self.hash_table
                if element != self._doom_value and element is not None]

    def update(self,
               dictionary: Optional[Dictionary] = None,
               **kwargs) -> None:
        if dictionary is not None:
            for key, value in dictionary.items():
                self[key] = value

        for key, value in kwargs.items():
            self[key] = value
