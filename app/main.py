from typing import Any, List, Tuple


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self._capacity: int = initial_capacity
        self._size: int = 0
        self._load_factor: float = 0.75
        self._buckets: List[List[Tuple[Any, int, Any]]] = [
            [] for _ in range(self._capacity)
        ]

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: Any, value: Any) -> None:
        h: int = hash(key)
        index: int = h % self._capacity
        bucket: List[Tuple[Any, int, Any]] = self._buckets[index]

        for i, (k, khash, v) in enumerate(bucket):
            if khash == h and k == key:
                bucket[i] = (key, h, value)
                return

        bucket.append((key, h, value))
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        h: int = hash(key)
        index: int = h % self._capacity
        bucket: List[Tuple[Any, int, Any]] = self._buckets[index]

        for k, khash, v in bucket:
            if khash == h and k == key:
                return v
        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        h: int = hash(key)
        index: int = h % self._capacity
        bucket: List[Tuple[Any, int, Any]] = self._buckets[index]

        for i, (k, khash, _) in enumerate(bucket):
            if khash == h and k == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def _resize(self) -> None:
        new_capacity: int = self._capacity * 2
        new_buckets: List[List[Tuple[Any, int, Any]]] = [
            [] for _ in range(new_capacity)
        ]

        for bucket in self._buckets:
            for k, h, v in bucket:
                new_index: int = h % new_capacity
                new_buckets[new_index].append((k, h, v))

        self._buckets = new_buckets
        self._capacity = new_capacity
