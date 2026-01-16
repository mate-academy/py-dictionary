from typing import Any, Iterable, Optional, Hashable


class Dictionary:

    def __init__(
            self,
            capacity: int = 8,
            load_factor: float = 0.75
    ) -> None:
        self.length: int = 0
        self.capacity: int = capacity
        self.load_factor: float = load_factor
        self.hash_table: list = [None] * capacity

    def __repr__(self) -> str:
        items = []
        for bucket in self.hash_table:
            if bucket:
                for key, value in bucket:
                    items.append(f"{key}: {value}")
        return "{" + ", ".join(items) + "}"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.get_index(key)
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.capacity
        if not self.hash_table[index]:
            self.hash_table[index] = [key, value]
            self.length += 1
        elif self.hash_table[index][0] == key:
            self.hash_table[index][1] = value
        if self.length >= self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index(key)
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key} not in hash table")

    def __iter__(self) -> Iterable:
        for bucket in self.hash_table:
            if bucket:
                for key, _ in bucket:
                    yield key

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        self.capacity *= 2
        new_hash = [None] * self.capacity
        for bucket in self.hash_table:
            if bucket and len(bucket) == 2:
                key, value = bucket
                index = self.get_index(key)
                while new_hash[index]:
                    index = (index + 1) % self.capacity
                new_hash[index] = [key, value]
        self.hash_table = new_hash

    def get(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value

    def __delitem__(self, key: Hashable) -> None:
        index = self.get_index(key)
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                del self.hash_table[index][0]
                self.length -= 1
                return
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key} not in hash table")
