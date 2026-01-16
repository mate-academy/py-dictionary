from typing import Any, Hashable, Iterable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.table: list = [None] * 8
        self.__capacity = len(self.table)

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.table = [None] * self.__capacity
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        hashed_key = hash(key)
        index = hashed_key % self.__capacity

        if self.table[index] is not None:
            for i, (k, h, v) in enumerate(self.table[index]):
                if k == key:
                    del self.table[index][i]
                    self.length -= 1
                    return

        raise KeyError(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hashed_key = hash(key)
        index = hashed_key % self.__capacity

        if self.table[index] is None:
            self.table[index] = []

        for i, (k, h, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, hashed_key, value)
                return

        self.table[index].append((key, hashed_key, value))
        self.length += 1

        if self.length >= self.__capacity * 2 / 3:
            self._resize()

    def _resize(self) -> None:
        old_table = self.table
        self.__capacity *= 2
        self.table = [None] * self.__capacity
        self.length = 0

        for bucket in old_table:
            if bucket is not None:
                for key, hashed_key, value in bucket:
                    self[key] = value

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.__capacity
        if self.table[index] is not None:
            for k, h, v in self.table[index]:
                if k == key:
                    return v
        raise KeyError(f"Key {key} not in hash table")

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def pop(self, key: Hashable, default: Any = None) -> None:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            else:
                raise

    def __iter__(self) -> Iterable:
        for bucket in self.table:
            if bucket:
                for key, _, value in bucket:
                    yield key
