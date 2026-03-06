from typing import Any, List, Optional, Tuple


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.count: int = 0
        self.load_factor: float = 0.75
        self.buckets: List[
            Optional[List[Tuple[Any, int, Any]]]] = [None] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        h: int = hash(key)
        index: int = h % self.capacity
        bucket: Optional[List[Tuple[Any, int, Any]]] = self.buckets[index]

        if bucket is None:
            self.buckets[index] = [(key, h, value)]
            self.count += 1
        else:
            for i, (k, kh, v) in enumerate(bucket):
                if k == key:
                    bucket[i] = (k, kh, value)
                    return
            bucket.append((key, h, value))
            self.count += 1

        if self.count > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        h: int = hash(key)
        index: int = h % self.capacity
        bucket: Optional[List[Tuple[Any, int, Any]]] = self.buckets[index]

        if bucket is None:
            raise KeyError(key)

        for k, kh, v in bucket:
            if k == key:
                return v

        raise KeyError(key)

    def __len__(self) -> int:
        return self.count

    def _resize(self) -> None:
        old_buckets: List[Optional[List[Tuple[Any, int, Any]]]] = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.count = 0

        for bucket in old_buckets:
            if bucket:
                for key, h, value in bucket:
                    self[key] = value
