from typing import Any


class Dictionary:

    def __init__(self,
                 initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _get_index(self,
                   key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._get_index(key)
        bucket = self.buckets[index]

        for i, (key_check, value_check) in enumerate(bucket):
            if key_check == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > 0.66:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._get_index(key)
        bucket = self.buckets[index]

        for key_check, value_check in bucket:
            if key_check == key:
                return value_check

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for key, value in bucket:
                self.__setitem__(key, value)
