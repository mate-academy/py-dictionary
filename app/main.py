from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._buckets = [None] * capacity
        self._size = 0
        self._load_factor = 0.6

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self._capacity

        # Handle collision by linear probing
        while (self._buckets[index] is not None
               and self._buckets[index][0] != key):
            index = (index + 1) % self._capacity

        # If the key is not in the dictionary, increment the size
        if self._buckets[index] is None:
            self._size += 1

        # Add or update the key-value pair
        self._buckets[index] = [key, hash(key), value]

        # Resize the dictionary if the load factor exceeds the threshold
        if self._size > round(self._capacity * self._load_factor):
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self._capacity

        # Search for the key in the dictionary
        while self._buckets[index] is not None:
            if self._buckets[index][0] == key:
                return self._buckets[index][2]
            index = (index + 1) % self._capacity

        # If the key is not found, raise a KeyError
        raise KeyError

    def _resize(self) -> None:
        self._capacity *= 2
        last_buckets = self._buckets
        self.clear()
        for bucket in last_buckets:
            if bucket is not None:
                self.__setitem__(bucket[0], bucket[2])
        del last_buckets

    def __len__(self) -> int:
        return self._size

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._size = 0

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self._capacity
        # Search for the key in the dictionary
        if self._buckets[index] is None:
            raise KeyError
        for _key, _hash, _value in self._buckets[index]:
            if _key == key and _hash == hash(key):
                self._buckets[index] = None
                self._size -= 1
                return

        raise KeyError

    def get(self, key: Hashable) -> Any:
        return self.__getitem__(key)

    def pop(self, key: Hashable, default: None = None) -> Any:
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
            return value
        except KeyError:
            return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Any:
        for bucket in self._buckets:
            if bucket is not None:
                key, _, value = bucket
                yield key
