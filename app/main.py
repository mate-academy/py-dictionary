from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.table = [None] * self.capacity
        self.length = 0

    def insert_into_hash_table(self, key: Hashable, value: Any) -> None:
        hash_value = hash(key) % self.capacity
        while (
                self.table[hash_value] is not None
                and self.table[hash_value][0] != key
        ):
            hash_value = (hash_value + 1) % self.capacity
        if (
                self.table[hash_value] is not None
                and self.table[hash_value][0] == key
        ):
            self.table[hash_value] = (key, hash_value, value)
        else:
            self.table[hash_value] = (key, hash_value, value)
            self.length += 1

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.insert_into_hash_table(key, value)
        if self.length >= self.load_factor * self.capacity:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key) % self.capacity
        for _ in range(self.capacity):
            if self.table[hash_value] is None:
                raise KeyError(f"Ключ '{key}' не знайдено в словнику")
            if self.table[hash_value][0] == key:
                return self.table[hash_value][2]
            hash_value = (hash_value + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for entry in self.table:
            if entry is not None:
                key, _, value = entry
                new_hash_value = hash(key) % new_capacity
                while new_table[new_hash_value] is not None:
                    new_hash_value = (new_hash_value + 1) % new_capacity
                new_table[new_hash_value] = (key, new_hash_value, value)

        self.table = new_table
        self.capacity = new_capacity
