from typing import Any


class Dictionary:
    hash_table: list[tuple[Any, int, Any] | None]
    length: int
    capacity: int

    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length / self.capacity >= 2 / 3:
            self._resize()

        key_hash: int = hash(key)
        index: int = key_hash % self.capacity

        while self.hash_table[index] is not None:
            entry = self.hash_table[index]
            if entry is not None and entry[0] == key:
                self.hash_table[index] = (key, key_hash, value)
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = (key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash: int = hash(key)
        index: int = key_hash % self.capacity

        while self.hash_table[index] is not None:
            entry = self.hash_table[index]
            if entry is not None and entry[0] == key:
                return entry[2]
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} not found")

    def _resize(self) -> None:
        self.capacity *= 2
        old_table: list[tuple[Any, int, Any] | None] = self.hash_table
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self[node[0]] = node[2]
