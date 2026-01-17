from typing import Any, Hashable


class Dictionary:
    def __init__(
            self, initial_capacity: int = 8, load_factor: float = 0.75
    ) -> None:
        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._size = 0
        self._buckets = [[] for _ in range(self._capacity)]

    def __hash_index(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def __resize(self) -> None:
        new_capacity = self._capacity * 2
        new_buckets = [[] for _ in range(new_capacity)]

        for bucket in self._buckets:
            for key, hash_key, value in bucket:
                new_index = hash_key % new_capacity
                new_buckets[new_index].append((key, hash_key, value))

        self._buckets = new_buckets
        self._capacity = new_capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._size / self._capacity > self._load_factor:
            self.__resize()

        hash_key = hash(key)
        index = self.__hash_index(key)
        bucket = self._buckets[index]

        for i, (new_key, new_hash_key, new_value) in enumerate(bucket):

            if new_key == key:
                bucket[i] = (key, hash_key, value)
                return
        bucket.append((key, hash_key, value))
        self._size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__hash_index(key)
        bucket = self._buckets[index]

        for new_key, new_hash_key, new_value in bucket:
            if new_key == key:
                return new_value

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self._size
