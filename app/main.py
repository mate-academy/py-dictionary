from __future__ import annotations
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.__max_capacity__ = 8
        self.__capacity__ = [None for _ in range(self.__max_capacity__)]
        self.__load_factor__ = 5
        self._size = 0
        self.__keys__ = []

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._size > self.__load_factor__:
            capacity = self.__capacity__.copy()

            self.__max_capacity__ = self.__max_capacity__ * 2
            self.__capacity__ = [None for _ in range(self.__max_capacity__)]

            self.__load_factor__ = int(self.__max_capacity__ * 2 / 3)

            self._size = 0

            for item in capacity:
                if isinstance(item, tuple):
                    self.__setitem__(item[0], item[1])

        hash_key = hash(key)

        stay_number = hash_key % self.__max_capacity__

        if not isinstance(self.__capacity__[stay_number], tuple):
            self.__capacity__[stay_number] = (key, value, hash_key)
            self._size += 1
            self.__keys__.append(key)

        else:
            existing = self.__capacity__[stay_number]
            if existing[0] == key:
                self.__capacity__[stay_number] = (key, value, hash_key)

            else:
                index = stay_number
                for max_operation in range(self.__max_capacity__):
                    index += 1
                    if index == self.__max_capacity__:
                        index = 0

                    if not isinstance(self.__capacity__[index], tuple):
                        self.__capacity__[index] = (key, value, hash_key)
                        self._size += 1
                        self.__keys__.append(key)
                        return

                    elif self.__capacity__[index][0] == key:
                        self.__capacity__[index] = (key, value, hash_key)
                        return

    def __getitem__(self, item: Any) -> Any:
        if item not in self.__keys__:
            raise KeyError(f"Not existing the key '{item}'")

        hash_key = hash(item)
        stay_number = hash_key % self.__max_capacity__

        value = self.__capacity__[stay_number]

        if isinstance(value, tuple):
            if value[0] == item and value[2] == hash_key:
                return value[1]

            elif value[0] != item:
                index = stay_number
                for max_operation in range(self.__max_capacity__):
                    index += 1
                    if index == self.__max_capacity__:
                        index = 0

                    value = self.__capacity__[index]
                    if value is None:
                        raise KeyError(f"Not existing the key '{item}'")
                    if value[0] == item and value[2] == hash_key:
                        return value[1]

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:

        return "{" + ", ".join(f"{item[0]}: {item[1]}"
                               for item in self.__capacity__
                               if isinstance(item, tuple)) + "}"

    def __delitem__(self, key: Any) -> None:
        return self.pop(key)

    def __iter__(self) -> Any:
        for item in self.__capacity__:
            if isinstance(item, tuple):
                yield item[0]

    def clear(self) -> None:
        self.__max_capacity__ = 8
        self.__capacity__ = [None for _ in range(self.__max_capacity__)]
        self.__load_factor__ = int(self.__max_capacity__ * 2 / 3)
        self._size = 0

    def get(self, key: Any) -> Any:
        if key not in self.__keys__:
            return None

        try:
            value = self[key]
            return value
        except KeyError:
            return None

    def pop(self, key: Any) -> None:
        if key not in self.__keys__:
            raise KeyError(f"Not existing the key '{key}'")

        index = hash(key) % self.__max_capacity__

        for _ in range(self.__max_capacity__):
            if index == self.__max_capacity__:
                index = 0

            value = self.__capacity__[index]
            if value is not None:
                if value[0] == key:
                    self.__capacity__[index] = None
                    self._size -= 1
                    self.__keys__.remove(key)

            index += 1

    def update(self, items: Any) -> None:
        for item in items:
            self[item] = items[item]
