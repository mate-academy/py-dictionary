from __future__ import annotations
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.load_factor = 2 / 3
        self.capacity = 8
        self.storage: list = [None] * 8
        self.length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_code = hash(key)
        data = (key, hash_code, value)
        index = hash_code % self.capacity

        for i in range(len(self.storage)):
            if self.storage[i] and key == self.storage[i][0]:
                self.storage[i] = data
                return

        if not self.storage[index]:
            self.storage[index] = data

        else:
            for i in range(len(self.storage)):
                if not self.storage[i]:
                    self.storage[i] = data
                    break

        self.length += 1
        self._resize()

    def __getitem__(self, key: Hashable) -> Any | Exception:
        for item in self.storage:
            if item:
                key_, hash_code, value = item
                if hash(key) == hash_code and key == key_:
                    return value
        raise KeyError(f"Dictionary has not key {key}")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None | Exception:
        for item in self.storage:
            if item and key in item:
                self.storage.remove(item)
                self.length -= 1
                return
        raise self[key]

    def __iter__(self) -> Dictionary:
        self._index = 0
        self._clean_storage = [item[2] for item in self.storage if item]
        return self

    def __next__(self) -> Any | Exception:
        index = self._index
        if self._index > len(self):
            self._index = 0
            self._clean_storage.clear()
            raise StopIteration
        self._index += 1
        return self._clean_storage[index]

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Hashable, default: Any = None) -> Any | None:
        for item in self.storage:
            if item and key in item:
                return item[2]
        return default

    def pop(self, key: Hashable, default: Any = None) -> Any | Exception:
        return_value = self.get(key)
        try:
            del self[key]
        except KeyError:
            if default:
                return default
            raise KeyError(f"Dictionary has not key {key}")
        return return_value

    def update(self, new_pair: list[tuple]) -> None:
        for pair in new_pair:
            self[pair[0]] = pair[1]

    def _resize(self) -> None:
        if self.length > (self.capacity * self.load_factor):
            reindex = [item for item in self.storage if item]
            self.storage.clear()
            self.length = 0
            self.capacity *= 2
            self.storage = [None] * self.capacity
            for item in reindex:
                self.__setitem__(item[0], item[2])
