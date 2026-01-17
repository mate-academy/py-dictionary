import dataclasses
from typing import Hashable, Any
from dataclasses import field


@dataclasses.dataclass
class Dictionary:
    length: int = 0
    capacity: int = 8
    constant_resize: float = 2 / 3
    hash_table: list = field(init=False)

    def __post_init__(self) -> None:
        self.hash_table = [None] * self.capacity

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _find_slot(self, key: Hashable) -> int:
        index = self._hash(key)
        while True:
            if self.hash_table[index] is None \
                    or self.hash_table[index][0] == key:
                return index
            index = (index + 1) % self.capacity

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.length = 0
        self.hash_table = [None] * self.capacity

        for element in old_hash_table:
            if element is not None:
                key, _, value = element
                index = self._find_slot(key)
                self.hash_table[index] = (key, self._hash(key), value)
                self.length += 1

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._find_slot(key)
        if self.hash_table[index] is None:
            self.length += 1
        self.hash_table[index] = (key, self._hash(key), value)
        if self.length / self.capacity > self.constant_resize:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._hash(key)

        for _ in range(self.capacity):
            if self.hash_table[index] is None:
                raise KeyError(f"Key {key} does not exist")
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} does not exist")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        index = self._hash(key)
        for _ in range(self.capacity):
            if self.hash_table[index] is None:
                raise KeyError(f"Key {key} does not exist")
            if self.hash_table[index][0] == key:
                break
            index = (index + 1) % self.capacity
        self.hash_table[index] = None
        self.length -= 1

        next_index = (index + 1) % self.capacity
        while self.hash_table[next_index] is not None:
            changed_key, changed_hash, changed_value \
                = self.hash_table[next_index]
            self.hash_table[next_index] = None
            self.length -= 1
            self[changed_key] = changed_value
            next_index = (next_index + 1) % self.capacity
