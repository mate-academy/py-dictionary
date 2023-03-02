from typing import Any, Iterable, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.67) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.threshold = int(self.capacity * self.load_factor)
        self.length = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_key = hash(key)
        index = hash_key % len(self.hash_table)
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % len(self.hash_table)
        if self.hash_table[index] and self.hash_table[index][0] == key:
            self.hash_table[index] = (key, hash_key, value)
        else:
            self.hash_table[index] = (key, hash_key, value)
            self.length += 1
            if self.length >= self.threshold:
                self.resize()

    def __getitem__(self, key: Hashable) -> None:
        index = hash(key) % len(self.hash_table)
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % len(self.hash_table)
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.capacity *= 2
        old_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.threshold = int(self.capacity * self.load_factor)
        self.length = 0
        for key_hash_value in old_table:
            if key_hash_value:
                self[key_hash_value[0]] = key_hash_value[2]

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % len(self.hash_table)
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = None
                self.length -= 1
                return
            index = (index + 1) % len(self.hash_table)
        raise KeyError(key)

    def get(self, key: Hashable, default: None = None) -> None:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def pop(self, key: Hashable, default: None = None) -> None:
        if self[key]:
            value = self[key]
            del self[key]
            return value
        if default:
            return default
        raise KeyError(key)

    def update(self, other: [dict | Iterable]) -> None:
        if isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
                break
        for key, value in other:
            self[key] = value
            break

    def __iter__(self) -> None:
        for key_hash_value in self.hash_table:
            if key_hash_value:
                yield key_hash_value[0]
