from typing import Any, NamedTuple


class _Entry(NamedTuple):
    key: Any
    hash_value: int
    value: Any


class Dictionary:
    _INITIAL_CAPACITY = 8
    _MAX_LOAD_FACTOR = 0.75

    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list[list[_Entry]] = [
            [] for _ in range(self._INITIAL_CAPACITY)
        ]

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        bucket = self.hash_table[key_hash % len(self.hash_table)]

        for index, entry in enumerate(bucket):
            if entry.hash_value == key_hash and entry.key == key:
                bucket[index] = _Entry(key, key_hash, value)
                return

        bucket.append(_Entry(key, key_hash, value))
        self.length += 1
        if self.length / len(self.hash_table) > self._MAX_LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        bucket = self.hash_table[key_hash % len(self.hash_table)]

        for entry in bucket:
            if entry.hash_value == key_hash and entry.key == key:
                return entry.value

        raise KeyError(f"Key {key!r} not found")

    def _resize(self) -> None:
        new_capacity = len(self.hash_table) * 2
        new_table: list[list[_Entry]] = [[] for _ in range(new_capacity)]

        for bucket in self.hash_table:
            for entry in bucket:
                new_table[entry.hash_value % new_capacity].append(entry)

        self.hash_table = new_table
