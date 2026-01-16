from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 0.67) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.length = 0
        self.hash_table: list[Any] = [None] * capacity

    def __len__(self) -> int:
        return self.length

    def get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> Any:
        if self.length / self.capacity >= self.load_factor:
            self.resize()

        index = self.get_index(key)

        if self.hash_table[index] and self.hash_table[index][0] == key:
            self.hash_table[index] = (key, index, value)
        else:
            self.length += 1
            self.hash_table[index] = (key, index, value)

    def resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table: list[Any] = [None] * self.capacity
        self.length = 0

        for item in old_table:
            if item:
                key, index, value = item
                self.__setitem__(key, value)

    def __getitem__(self, key: Hashable) -> Any | None:
        index = self.get_index(key)

        if not self.hash_table[index]:
            raise KeyError(f"Key {key} not found")
        if self.hash_table[index][0] == key:
            return self.hash_table[index][2]

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index] is None:
            index = (index + 1) * self.capacity
            if self.hash_table[index][0] == key:
                del self.hash_table[index]
                self.length -= 1
                return

            raise KeyError(f"Key {key} not found2")

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        index = self.get_index(key)
        if self.hash_table[index] is None:
            return default_value
        return self.hash_table[index][2]
