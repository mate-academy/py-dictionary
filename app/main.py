from typing import Any


class Dictionary:

    class _Node:
        def __init__(self, key: Any, value: Any) -> None:
            self.key = key
            self.value = value

    def __init__(self) -> None:
        self._initial_capacity = 8
        self._size = 0
        self._buckets = [[] for _ in range(self._initial_capacity)]

    def _bucket_index(self, key: Any) -> int:
        return hash(key) % len(self._buckets)

    def __setitem__(self, key: Any, value: Any) -> None:
        index = self._bucket_index(key)
        bucket = self._buckets[index]

        for node in bucket:
            if node.key == key:
                node.value = value
                return

        bucket.append(self._Node(key, value))
        self._size += 1

        if self._size / len(self._buckets) > 0.75:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index = self._bucket_index(key)
        bucket = self._buckets[index]

        for node in bucket:
            if node.key == key:
                return node.value

        raise KeyError(f"Klucz {key} nie istnieje w słowniku.")

    def __len__(self) -> int:
        return self._size

    def _resize(self) -> None:
        old_buckets = self._buckets
        new_capacity = len(self._buckets) * 2
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value
