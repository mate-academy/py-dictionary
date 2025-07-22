from typing import Any


class Node:
    def __init__(
            self,
            key: Any,
            value: Any
    ) -> None:
        self.key = key
        self.key_hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.load_factor = 2 / 3
        self.capacity = 8
        self.hash_table: list[Node | None] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= int(self.capacity * self.load_factor):
            self._resize()

        idx = self._get_index(key)
        if self.hash_table[idx] is None:
            self._write_to_hash_table(idx, key, value)
            return

        while self.hash_table[idx]:
            if self.hash_table[idx].key == key:
                self.hash_table[idx].value = value
                return
            idx = (idx + 1) % self.capacity
        self._write_to_hash_table(idx, key, value)

    def __getitem__(self, key: Any) -> Any:
        idx = self._get_index(key)
        while self.hash_table[idx]:
            if self.hash_table[idx].key == key:
                return self.hash_table[idx].value
            idx = (idx + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.length = 0
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for item in old_hash_table:
            if item is not None:
                self[item.key] = item.value

    def _get_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def _write_to_hash_table(
            self,
            idx: int,
            key: Any,
            value: Any
    ) -> None:
        self.hash_table[idx] = Node(key, value)
        self.length += 1

    def get(self, key: Any, default_value: Any = None) -> Any:
        idx = self._get_index(key)
        while self.hash_table[idx]:
            if self.hash_table[idx].key == key:
                return self.hash_table[idx].value
            idx = (idx + 1) % self.capacity
        return default_value

    def clear(self) -> None:
        self.length = 0
        self.hash_table = [None] * self.capacity

    def pop(self, key: Any, default_value: object = object()) -> Any:
        idx = self._get_index(key)
        while self.hash_table[idx]:
            if self.hash_table[idx].key == key:
                value = self.hash_table[idx].value
                self.hash_table[idx] = None
                self.length -= 1
                return value
            idx = (idx + 1) % self.capacity

        if default_value is not self.pop.__defaults__[0]:
            return default_value
        raise KeyError(key)
