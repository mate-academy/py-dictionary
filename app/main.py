from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.length = 0
        self.hash_table = [None] * self.capacity

    def _resize(self) -> None:
        old_table = self.hash_table

        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for bucket in old_table:
            if bucket is not None:
                for node in bucket:
                    self[node["key"]] = node["value"]

    def __setitem__(self, key: Any, value: Any) -> None:
        if (self.length + 1) / self.capacity > self.load_factor:
            self._resize()

        index = hash(key) % self.capacity

        if self.hash_table[index] is None:
            self.hash_table[index] = []

        for node in self.hash_table[index]:
            if node["key"] == key:
                node["value"] = value
                return

        self.hash_table[index].append({
            "key": key,
            "hash": hash(key),
            "value": value,
        })

        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity

        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} is not found")

        for node in self.hash_table[index]:
            if node["key"] == key:
                return node["value"]

        raise KeyError(f"Key {key} is not found")

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % self.capacity

        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} is not found")

        for i, node in enumerate(self.hash_table[index]):
            if node["key"] == key:
                del self.hash_table[index][i]
                self.length -= 1
                return

        raise KeyError(f"Key {key} is not found")

    def __len__(self) -> int:
        return self.length
