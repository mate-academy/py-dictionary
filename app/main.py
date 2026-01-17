from symtable import Class
from typing import Any


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 8,
            load_factor: float = 0.65
    ) -> None:
        self._capacity = initial_capacity
        self._default_capacity = initial_capacity
        self._size = 0
        self._load_factor = load_factor
        self._list = [[] for _ in range(self._capacity)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        old_list = self._list
        self._capacity *= 2
        self._list = [[] for _ in range(self._capacity)]
        self._size = 0

        for item in old_list:
            if isinstance(item, tuple):
                self[item[0]] = item[1]

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self._size + 1) / self._capacity > self._load_factor:
            self._resize()

        try:
            index = self._list.index((key, self[key]))
            self._list[index] = (key, value)
        except (KeyError, ValueError):
            index = self._hash(key)
            while self._list[index]:
                if index == self._capacity - 1:
                    index = 0
                else:
                    index += 1
            self._list[index] = (key, value)
            self._size += 1

    def __getitem__(self, key: Any) -> Any:
        for item in self._list:
            if isinstance(item, tuple) and item[0] == key:
                return item[1]

        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self._list = [[] for _ in range(self._default_capacity)]

    def __delitem__(self, key: Any) -> None:
        for i, item in enumerate(self._list):
            if isinstance(item, tuple) and item[0] == key:
                self._list[i] = []
                self._size -= 1

    def get(self, key: Any = 1) -> Any | None:
        for item in self._list:
            if item and item[0] == key:
                return item[1]

        return None

    def pop(self, key: Any = 1) -> Any | KeyError:
        try:
            result = self[key]
            self.__delitem__(key)
            return result
        except KeyError:
            raise

    def update(self, other: Class) -> None:
        for item in other._list:
            if isinstance(item, tuple):
                self.__setitem__(item[0], item[1])

    def __repr__(self) -> str:
        items = []
        for item in self._list:
            if isinstance(item, tuple):
                items.append(f"{item[0]}: {item[1]}")
        return "{" + ", ".join(items) + "}"
