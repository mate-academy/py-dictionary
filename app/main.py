from typing import Any
from typing import Iterator


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.initial_capacity = initial_capacity
        self.buckets = [{} for _ in range(initial_capacity)]

    @property
    def _load_factor(self) -> float:
        return len(self) / self.initial_capacity

    def _resize(self) -> None:
        if self._load_factor > 2 / 3:
            new_size = self.initial_capacity * 2
            new_buckets = [{} for _ in range(new_size)]
            for bucket in self.buckets:
                for key, value in bucket.items():
                    new_hash_key = hash(key) % new_size
                    new_buckets[new_hash_key][key] = value
            self.initial_capacity = new_size
            self.buckets = new_buckets
        else:
            self.initial_capacity = self.initial_capacity
            self.buckets = self.buckets

    def __setitem__(self, key: int, value: str) -> None:
        self._resize()
        hash_key = self._hash_function(key)
        bucket = self.buckets[hash_key]
        bucket[key] = value

    def __getitem__(self, key: Any) -> Any:
        hash_key = self._hash_function(key)
        if key in self.buckets[hash_key]:
            return self.buckets[hash_key][key]
        else:
            raise KeyError(key)

    def __len__(self) -> int:
        return sum(len(bucket) for bucket in self.buckets)

    def __list__(self) -> Any:
        data_list = []
        for bucket in self.buckets:
            data_list.extend(bucket)
        return data_list

    def clear(self) -> None:
        for bucket in self.buckets:
            bucket.clear()

    def pop(self, object_: dict, default_value: Any = None) -> Any:
        bucket_index = self._get_bucket_index(object_)
        bucket = self.buckets[bucket_index]
        for i, (stored_key, value) in enumerate(bucket):
            if stored_key == object_:
                del bucket[i]
                return value
        if default_value is not None:
            return default_value
        raise KeyError(object_)

    def update(self, object_: dict = None, **dict_) -> None:
        if object_ is not None:
            if hasattr(object_, "keys"):
                for key_, value_ in object_.items():
                    self[key_] = value_
            else:
                for key_, value_ in object_:
                    self[key_] = value_
        for key_, value_ in dict_.items():
            self[key_] = value_

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key: Any) -> None:
        for bucket in self.buckets:
            for i, (existing_key, existing_value) in enumerate(bucket):
                if existing_key == key:
                    del bucket[i]
                    return
        raise KeyError(key)

    def __iter__(self) -> Iterator:
        return iter(self.keys)

    def _hash_function(self, key: Any) -> int:
        hash_key_ = hash(key)
        return hash_key_ % self.initial_capacity
