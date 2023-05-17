from typing import Any


class Dictionary:
    def __init__(
        self, initial_capacity: int = 8, load_factor: float = 2 / 3
    ) -> None:
        self.initial_capacity = initial_capacity
        self.load_factor = load_factor
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(initial_capacity)]

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size / self.capacity > self.load_factor:
            self._resize()
        bucket_index = self._get_bucket_index(key)
        bucket = self.buckets[bucket_index]

        for i, (stored_key, stored_value, stored_hash) in enumerate(bucket):
            if stored_key == key:
                bucket[i] = (key, value, hash(key))
                return

        bucket.append((key, value, hash(key)))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        bucket_index = self._get_bucket_index(key)
        bucket = self.buckets[bucket_index]

        for stored_key, stored_value, stored_hash in bucket:
            if stored_key == key:
                return stored_value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _get_bucket_index(self, key: Any) -> int:
        hash_value = hash(key)
        initial_index = hash_value % self.capacity
        bucket_index = initial_index

        while bucket_index >= len(self.buckets):
            self._resize()

        bucket = self.buckets[bucket_index]

        while bucket:
            for stored_key, _, _ in bucket:
                if stored_key == key:
                    return bucket_index
            bucket_index = (bucket_index + 1) % self.capacity
            bucket = self.buckets[bucket_index]

            if bucket_index == initial_index:
                raise KeyError(key)

        return bucket_index

    def _resize(self) -> None:
        self.capacity *= 2
        new_buckets = [[] for _ in range(self.capacity)]

        for bucket in self.buckets:
            for key, value, _ in bucket:
                bucket_index = hash(key) % self.capacity
                new_buckets[bucket_index].append((key, value, hash(key)))

        self.buckets = new_buckets
