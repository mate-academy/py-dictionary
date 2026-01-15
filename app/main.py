from typing import Any, Hashable


class Dictionary:

    def __init__(
            self,
            initial_size: int = 8,
            expansion_factor: int = 2,
            load_factor: float = 0.7
    ) -> None:
        self._initial_size = initial_size
        self._expansion_factor = expansion_factor
        self._load_factor = load_factor
        self._array_buckets = [[] for _ in range(initial_size)]

    def _get_hash_code(self, key: Hashable) -> int:
        return hash(key) % len(self._array_buckets)

    def _resize_array(self) -> None:
        old_array = self._array_buckets
        new_size_array = len(old_array) * self._expansion_factor
        self._array_buckets = [
            [] for _ in range(new_size_array)
        ]

        for bucket in old_array:
            for key, value in bucket:
                index = hash(key) % new_size_array
                self._array_buckets[index].append((key, value))

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.__len__() >= len(self._array_buckets) * self._load_factor:
            self._resize_array()

        bucket = self._array_buckets[self._get_hash_code(key)]
        for index, (key_, _) in enumerate(bucket):
            if key_ == key:
                bucket[index] = (key, value)
                return
        bucket.append((key, value))

    def __getitem__(self, key: Hashable) -> Any:
        bucket = self._array_buckets[self._get_hash_code(key)]
        for key_, value_ in bucket:
            if key_ == key:
                return value_
        raise KeyError(f"Key {key} not found")

    def __repr__(self) -> str:
        return (
            "".join("".join(str(item) + ", " for item in bucket) for bucket in
                    self._array_buckets)
        )

    def __len__(self) -> int:
        return sum(len(bucket) for bucket in self._array_buckets)
