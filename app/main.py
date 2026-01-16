from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._load_factor = 2 / 3
        self._size = 0
        self.storage = [None] * self._capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        idx, hash_ = self.get_index_and_hash(key)
        while True:
            if self.storage[idx] is None:
                self.storage[idx] = (key, hash_, value)
                self._size += 1
                break
            if (
                key == self.storage[idx][0]
                and hash_ == self.storage[idx][1]
            ):
                self.storage[idx] = (key, hash_, value)
                break
            idx = (idx + 1) % self._capacity
        if self._size >= self._capacity * self._load_factor:
            self.resize()

    def __getitem__(self, key: Any) -> int:
        idx, hash_ = self.get_index_and_hash(key)
        end_idx = idx - 1
        while True:
            if (
                self.storage[idx] is not None
                and key == self.storage[idx][0]
                and hash_ == self.storage[idx][1]
            ):
                return self.storage[idx][2]
            if idx == end_idx:
                raise KeyError
            idx = (idx + 1) % self._capacity

    def __delitem__(self, key: Any) -> None:
        idx = 0
        for item in self.storage:
            if item is not None and item[0] == key:
                self.storage[idx] = None
                break
            idx += 1
        else:
            raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> None:
        for item in self.storage:
            if item is not None:
                yield item[0]

    def get_index_and_hash(self, key: Any) -> tuple:
        hash_ = hash(key)
        return hash_ % self._capacity, hash_

    def resize(self) -> None:
        old_storage = self.storage
        self._capacity *= 2
        self._size = 0
        self.clear()
        for item in old_storage:
            if item is not None:
                self.__setitem__(item[0], item[2])

    def clear(self) -> None:
        self.storage = [None] * self._capacity

    def get(self, key: Any, default: Any = None) -> None:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Any, *default) -> Any:
        try:
            result = self.__getitem__(key)
            self.__delitem__(key)
        except KeyError:
            if default:
                return default
            raise KeyError
        else:
            return result
