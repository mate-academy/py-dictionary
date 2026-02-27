from typing import Any, List


class Dictionary:
    INITIAL_CAPACITY: int = 8
    LOAD_FACTOR: float = 0.75

    class _Node:
        def __init__(self, key: Any, hash_value: int, value: Any) -> None:
            self.key: Any = key
            self.hash: int = hash_value
            self.value: Any = value

    def __init__(self) -> None:
        self._capacity: int = self.INITIAL_CAPACITY
        self._size: int = 0
        self._buckets: List[List[Dictionary._Node]] = [
            [] for _ in range(self._capacity)
        ]

    def __len__(self) -> int:
        return self._size

    def _get_index(self, hash_value: int) -> int:
        return hash_value % self._capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value: int = hash(key)
        index: int = self._get_index(hash_value)
        bucket: List[Dictionary._Node] = self._buckets[index]

        for node in bucket:
            if node.hash == hash_value and node.key == key:
                node.value = value
                return

        bucket.append(self._Node(key, hash_value, value))
        self._size += 1

        if self._size / self._capacity > self.LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value: int = hash(key)
        index: int = self._get_index(hash_value)
        bucket: List[Dictionary._Node] = self._buckets[index]

        for node in bucket:
            if node.hash == hash_value and node.key == key:
                return node.value

        raise KeyError(key)

    def _resize(self) -> None:
        old_buckets: List[List[Dictionary._Node]] = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

        for bucket in old_buckets:
            for node in bucket:
                self[node.key] = node.value
