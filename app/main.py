from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._size = 0
        self._load_factor = 2 / 3

        self._buckets = [[] for _ in range(self._capacity)]
        # Отримуємо список порожніх "відер" для хеш-таблиці

    def __len__(self) -> int:
        return self._size

    def _get_index(self, key: int) -> int:
        return hash(key) % self._capacity

    def __setitem__(self, key: int, value: Any) -> None:
        idx = self._get_index(key)
        bucket = self._buckets[idx]
        key_hash = hash(key)

        for i, (k, h, v) in enumerate(bucket):
            if h == key_hash and k == key:
                bucket[i] = (key, key_hash, value)
                return

        bucket.append((key, key_hash, value))
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def __getitem__(self, key: int) -> Any:
        idx = self._get_index(key)
        bucket = self._buckets[idx]
        key_hash = hash(key)

        for (k, h, v) in bucket:
            if h == key_hash and k == key:
                return v

        raise KeyError(f"Key {key!r} not found")

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]

        old_size = self._size
        self._size = 0

        for bucket in old_buckets:
            for (k, h, v) in bucket:
                idx = h % self._capacity
                self._buckets[idx].append((k, h, v))
                self._size += 1

        assert self._size == old_size
