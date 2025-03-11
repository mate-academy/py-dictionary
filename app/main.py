from typing import Any, List, Tuple


class Dictionary:
    def __init__(self, capacity: int = 8,
                 load_factor: float = 0.7) -> None:
        self.capacity: int = capacity
        self.size: int = 0
        self.load_factor: float = load_factor
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.capacity)]  # noqa: E501

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        index: int = self._hash(key)
        bucket: List[Tuple[Any, Any]] = self.table[index]

        if self.size >= self.capacity * self.load_factor:
            self._resize()

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        index: int = self._hash(key)
        bucket: List[Tuple[Any, Any]] = self.table[index]

        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity: int = self.capacity * 2
        new_table: List[List[Tuple[Any, Any]]] = [[] for _ in range(new_capacity)]  # noqa: E501

        for bucket in self.table:
            for key, value in bucket:
                index: int = hash(key) % new_capacity
                new_table[index].append((key, value))

        self.capacity = new_capacity
        self.table = new_table
