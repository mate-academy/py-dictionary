from collections.abc import Hashable
from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.__capacity = capacity
        self.__table = [[]for _ in range(capacity)]
        self.__load_factor = 0.75
        self._size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.__capacity
        bucket = self.__table[index]

        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return

        bucket.append([key, value])
        self._size += 1

        if self._size / self.__capacity > self.__load_factor:
            self.__resize()

    def __getitem__(self, key: Hashable) -> None:
        index = hash(key) % self.__capacity
        bucket = self.__table[index]

        for pair in bucket:
            if pair[0] == key:
                return pair[1]

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self._size

    def __resize(self) -> None:
        old_table = self.__table
        self.__capacity *= 2
        self.__table = [[] for _ in range(self.__capacity)]
        self._size = 0

        for bucket in old_table:
            for key, value in bucket:
                self[key] = value
