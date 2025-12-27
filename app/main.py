from typing import Any, Dict, Optional
from collections.abc import Hashable


class Node:
    def __init__(self, key: Hashable, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 0.67) -> None:
        self.initial_capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [[] for _ in range(self.initial_capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key) % self.initial_capacity
        for entry in self.table[hash_value]:
            if entry.key == key and entry.hash_value == hash_value:
                entry.value = value
                return
        self.table[hash_value].append(Node(key, hash_value, value))
        self.size += 1
        if self.size > self.initial_capacity * self.load_factor:
            self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key) % self.initial_capacity
        for entry in self.table[hash_value]:
            if entry.key == key:
                return entry.value
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        new_size = self.initial_capacity * 2
        new_table = [[] for _ in range(new_size)]
        for cell in self.table:
            for entry in cell:
                new_hash_value = hash(entry.key) % new_size
                new_table[new_hash_value].append(entry)
        self.table = new_table
        self.initial_capacity = new_size

    def clear(self) -> None:
        self.initial_capacity = 8
        self.size = 0
        self.table = [[] for _ in range(self.initial_capacity)]

    def __delitem__(self, key: Hashable) -> None:
        hash_value = hash(key) % self.initial_capacity
        for index, entry in enumerate(self.table[hash_value]):
            if entry.key == key and entry.hash_value == hash_value:
                del self.table[hash_value][index]
                self.size -= 1
                return

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
            if default is None:
                raise
            return default

    def update(self, other_dict: Dict[Any, Any]) -> None:
        for key, value in other_dict.items():
            self[key] = value

    def __iter__(self) -> None:
        for bucket in self.table:
            for entry in bucket:
                yield entry.key, entry.value
