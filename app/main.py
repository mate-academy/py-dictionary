from typing import Any, List, Tuple, Hashable


class Dictionary:

    def __init__(self, size: int = 8) -> None:
        self.data = size
        self.buckets = [[] for _ in range(self.data)]
        self.load_factor = 2 / 3
        self.total_count = 0

    def hash_data(self, key: Hashable) -> int:
        return hash(key) % self.data

    def __setitem__(self, key: Any, value: Any) -> None:
        key_hash = self.hash_data(key)
        for i, (k, v) in enumerate(self.buckets[key_hash]):
            if k == key:
                self.buckets[key_hash][i] = (key, value)
                return
        self.buckets[key_hash].append((key, value))
        self.total_count += 1

    def __getitem__(self, key: Any) -> Any:
        key_hash = self.hash_data(key)
        for k, v in self.buckets[key_hash]:
            if k == key:
                return v
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        total_count = 0
        for bucket in self.buckets:
            total_count += len(bucket)
        return total_count

    def __resize__(self) -> None:
        new_size = 2 * self.data
        new_bucket: List[List[Tuple[Any, Any]]] = [[] for _ in range(new_size)]

        for bucket in self.buckets:
            for k, v in bucket:
                new_key_hash = self.hash_data(k)
                new_bucket[new_key_hash].append((k, v))

        self.data = new_size
        self.buckets = new_bucket
