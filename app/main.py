from typing import Any, Iterable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.load_factor = 2 / 3
        self.hash_table = [[] for _ in range(self.capacity)]

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [[] for _ in range(self.capacity)]
        for bucket in old_hash_table:
            for key, value in bucket:
                index = hash(key) % self.capacity
                self.hash_table[index].append((key, value))

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * self.load_factor:
            self._resize()
        index = hash(key) % self.capacity
        bucket = self.hash_table[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.length += 1

    def __getitem__(self, key: Any) -> Any:
        bucket = self.hash_table[hash(key) % self.capacity]
        for key_, value_ in bucket:
            if key_ == key:
                return value_
        raise KeyError("Such key doesn't exist")

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Any) -> None:
        bucket = self.hash_table[hash(key) % self.capacity]
        for i, (key_, value_) in enumerate(bucket):
            if key_ == key:
                del bucket[i]
                self.length -= 1
                return
        raise KeyError(f"Key '{key}' doesn't exist")

    def __iter__(self) -> Any:
        for bucket in self.hash_table:
            for key_, value_ in bucket:
                yield key_

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self.capacity)]
        self.length = 0

    def get(self, key: Any, default: Any = None) -> Any:
        bucket = self.hash_table[hash(key) % self.capacity]
        for key_, value_ in bucket:
            if key_ == key:
                return value_
        return default

    def pop(self, key: Any, *args) -> Any:
        bucket = self.hash_table[hash(key) % self.capacity]
        for key_, value_ in bucket:
            if key_ == key:
                item = value_
                bucket.remove((key_, value_))
                self.length -= 1
                return item
        if args:
            return args[0]
        raise KeyError("Such key doesn't exist")

    def update(self, other: Any | Iterable = None, **kwargs) -> None:
        if other is not None:
            if hasattr(other, "keys"):
                for key_ in other.keys():
                    self[key_] = other[key_]
            else:
                for key_, value_ in other:
                    self[key_] = value_
        for key_, value_ in kwargs.items():
            self[key_] = value_
