from typing import Any


class Dictionary:
    DELETED = object()

    def __init__(self) -> None:
        self.hash_table = [None] * 8
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        bucket_index = hash(key) % len(self.hash_table)
        first_deleted = None
        start_index = bucket_index  # ← запам'ятали старт

        while self.hash_table[bucket_index] is not None:
            slot = self.hash_table[bucket_index]
            if slot is Dictionary.DELETED:
                if first_deleted is None:
                    first_deleted = bucket_index
            elif slot[0] == key:
                self.hash_table[bucket_index] = (key, hash(key), value)
                return
            bucket_index = (bucket_index + 1) % len(self.hash_table)
            if bucket_index == start_index:  # ← пройшли повне коло
                break

        target = first_deleted if first_deleted is not None else bucket_index
        self.hash_table[target] = (key, hash(key), value)
        self.length += 1

        if self.length / len(self.hash_table) >= 2 / 3:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        bucket_index = hash(key) % len(self.hash_table)
        start_index = bucket_index

        while self.hash_table[bucket_index] is not None:
            slot = self.hash_table[bucket_index]
            if slot is not Dictionary.DELETED and slot[0] == key:
                return slot[2]
            bucket_index = (bucket_index + 1) % len(self.hash_table)
            if bucket_index == start_index:
                break

        raise KeyError(f"Key {key} not in dictionary")

    def __delitem__(self, key: Any) -> None:
        bucket_index = hash(key) % len(self.hash_table)
        start_index = bucket_index

        while self.hash_table[bucket_index] is not None:
            slot = self.hash_table[bucket_index]
            if slot is not Dictionary.DELETED and slot[0] == key:
                self.hash_table[bucket_index] = Dictionary.DELETED
                self.length -= 1
                return
            bucket_index = (bucket_index + 1) % len(self.hash_table)
            if bucket_index == start_index:
                break

        raise KeyError(f"Key {key} not in dictionary")

    def __iter__(self) -> Any:
        for slot in self.hash_table:
            if slot is not None and slot is not Dictionary.DELETED:
                yield slot[0]

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.hash_table = [None] * len(old_hash_table) * 2
        self.length = 0
        for slot in old_hash_table:
            if slot is not None and slot is not Dictionary.DELETED:
                self[slot[0]] = slot[2]

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.length = 0

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any, *args: Any) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if args:
                return args[0]
            raise KeyError(f"Key {key} not in dictionary")

    def update(self, other: Any = None, **kwargs: Any) -> None:
        if other is not None:
            for key in other:
                self[key] = other[key]
        for key, value in kwargs.items():
            self[key] = value
