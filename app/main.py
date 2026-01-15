from typing import Any


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0
        self.load_factor_threshold = 0.66

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        bucket = self.table[index]

        for i, (existing_key, existing_value, existing_hash) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value, key_hash)
                return
        bucket.append((key, value, key_hash))
        self.size += 1

        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        bucket = self.table[index]

        for existing_key, value, existing_hash in bucket:
            if existing_key == key:
                return value
        raise KeyError(f"Key '{key}' not found in dictionary")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]
        old_table = self.table
        self.table = new_table
        self.capacity = new_capacity
        self.size = 0
        for bucket in old_table:
            for key, value, old_hash in bucket:
                new_index = old_hash % self.capacity
                self.table[new_index].append((key, value, old_hash))
                self.size += 1
        print(
            f"Resizing done. New capacity: {self.capacity}."
            f" Size remains: {self.size}"
        )
