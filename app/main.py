from typing import Any

import hashable as hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.hash_capacity = 8

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return str(self.hash_table)

    def __setitem__(self, key: hashable, value: Any) -> None:
        if self.length <= round(self.hash_capacity * 2 / 3):
            index = self._get_index(key)
            if self.hash_table[index] is None:
                self.hash_table[index] = (key, value, hash(key))
                self.length += 1
            else:
                self.hash_table[index] = (key, value, hash(key))
        else:
            self.resize()
            self[key] = value

    def resize(self) -> None:
        self.hash_capacity *= 2
        hash_table = self.hash_table.copy()
        self.hash_table = [None] * self.hash_capacity
        self.length = 0
        for place in hash_table:
            if place:
                self[place[0]] = place[1]

    def __getitem__(self, key: hashable) -> Any:
        index = self._get_index(key)
        if self.hash_table[index] and self._check_key(key, index):
            return self.hash_table[index][1]
        raise KeyError(f"There is no element with this key: {key}")

    def _get_index(self, key: hashable) -> int:
        index = hash(key) % self.hash_capacity
        while (self.hash_table[index] is not None
                and not self._check_key(key, index)):
            index = (index + 1) % self.hash_capacity
        return index

    def _check_key(self, key: hashable, index: int) -> bool:
        return (hash(key) == self.hash_table[index][2]
                and self.hash_table[index][0] == key)

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.length = 0

    def __delitem__(self, key: hashable) -> None:
        if self[key]:
            index = self._get_index(key)
            self.hash_table[index] = None
        else:
            raise KeyError(f"Wrong key: {key}")

    def get(self, key: hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: hashable, default: Any = None) -> Any:
        try:
            pop_value = self[key]
            del self[key]
            return pop_value
        except KeyError:
            if not default:
                raise
            else:
                return default

    def update(self, *args) -> None:
        update_data, = args
        if type(update_data) == dict:
            for key, value in update_data.items():
                self[key] = value
        else:
            for pair in update_data:
                key, value = pair
                self[key] = value

    def __iter__(self) -> hashable:
        for el in self.hash_table:
            if el:
                yield el[0]
