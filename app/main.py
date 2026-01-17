from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.buckets = [[] for _ in range(self.capacity)]
        self.load_factor = 2 / 3
        self.total_count = 0

    def hash_data(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = self.hash_data(key)
        for i, (exist_key, exist_value) in enumerate(self.buckets[key_hash]):
            if exist_key == key:
                self.buckets[key_hash][i] = (key, value)
                return
        self.buckets[key_hash].append((key, value))
        self.total_count += 1
        if self.total_count >= self.capacity * self.load_factor:
            self.__resize__()

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = self.hash_data(key)
        for exist_key, exist_value in self.buckets[key_hash]:
            if exist_key == key:
                return exist_value
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.total_count

    def __resize__(self) -> None:
        new_size = 2 * self.capacity
        new_buckets = [[] for _ in range(new_size)]

        for bucket in self.buckets:
            for key, value in bucket:
                new_index = hash(key) % new_size
                new_buckets[new_index].append((key, value))

        self.capacity = new_size
        self.buckets = new_buckets
