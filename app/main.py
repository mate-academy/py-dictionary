from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        self.load_factor_threshold = 0.75

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        bucket = self.buckets[index]

        # Проверяем, есть ли уже ключ
        for i, (k, h, v) in enumerate(bucket):
            if h == key_hash and k == key:
                bucket[i] = (key, key_hash, value)
                return

        # Добавляем новый элемент
        bucket.append((key, key_hash, value))
        self.size += 1

        # Проверяем load factor
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        bucket = self.buckets[index]

        for k, h, v in bucket:
            if h == key_hash and k == key:
                return v

        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_buckets:
            for key, key_hash, value in bucket:
                index = key_hash % self.capacity
                self.buckets[index].append((key, key_hash, value))
                self.size += 1
