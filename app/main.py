from typing import TypeVar, Generic, Hashable, Iterator

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class Dictionary(Generic[K, V]):
    def __init__(self) -> None:
        self._initial_capacity: int = 8
        self._load_factor: float = 0.75
        self._buckets: list[list[tuple[int, K, V]]] = [
            [] for _ in range(self._initial_capacity)
        ]
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def __setitem__(self, key: K, value: V) -> None:
        if self._length + 1 > len(self._buckets) * self._load_factor:
            self._resize()
        self._insert(key, value)

    def __getitem__(self, key: K) -> V:
        key_hash: int = hash(key)
        bucket: list[tuple[int, K, V]] = self._get_bucket(key_hash)
        for h, k, v in bucket:
            if h == key_hash and k == key:
                return v
        raise KeyError(f"Key {key!r} not found")

    def __delitem__(self, key: K) -> None:
        key_hash: int = hash(key)
        bucket: list[tuple[int, K, V]] = self._get_bucket(key_hash)
        for i, (h, k, _) in enumerate(bucket):
            if h == key_hash and k == key:
                del bucket[i]
                self._length -= 1
                return
        raise KeyError(f"Key {key!r} not found")

    def get(self, key: K, default: V | None = None) -> V | None:
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, other: "Dictionary[K, V]") -> None:
        for key in other:
            self[key] = other[key]

    def pop(self, key: K) -> V:
        key_hash: int = hash(key)
        bucket: list[tuple[int, K, V]] = self._get_bucket(key_hash)
        for i, (h, k, v) in enumerate(bucket):
            if h == key_hash and k == key:
                del bucket[i]
                self._length -= 1
                return v
        raise KeyError(f"Key {key!r} not found")

    def clear(self) -> None:
        for i in range(len(self._buckets)):
            self._buckets[i].clear()
        self._length = 0

    def __iter__(self) -> Iterator[K]:
        for bucket in self._buckets:
            for _, k, _ in bucket:
                yield k

    def _get_bucket(self, key_hash: int) -> list[tuple[int, K, V]]:
        index: int = key_hash % len(self._buckets)
        return self._buckets[index]

    def _insert(self, key: K, value: V) -> None:
        key_hash: int = hash(key)
        bucket: list[tuple[int, K, V]] = self._get_bucket(key_hash)
        for i, (h, k, _) in enumerate(bucket):
            if h == key_hash and k == key:
                bucket[i] = (key_hash, key, value)
                return
        bucket.append((key_hash, key, value))
        self._length += 1

    def _resize(self) -> None:
        old_buckets: list[list[tuple[int, K, V]]] = self._buckets
        new_capacity: int = len(self._buckets) * 2
        self._buckets = [[] for _ in range(new_capacity)]
        self._length = 0

        for bucket in old_buckets:
            for _, k, v in bucket:
                self._insert(k, v)
