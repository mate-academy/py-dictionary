from typing import Any


class Dictionary:

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.data = [[] for _ in range(capacity)]
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        _hash = hash(key)
        index = _hash % self.capacity
        bucket = self.data[index]
        load_factor = (self.size + 1) / self.capacity

        for i, (k, v, h) in enumerate(bucket):
            if h == _hash:
                if k == key:
                    bucket[i] = (key, value, _hash)
                    return

        if load_factor > 2 / 3:
            self._resize()
            index = _hash % self.capacity
            bucket = self.data[index]

        bucket.append((key, value, _hash))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        _hash = hash(key)
        index = _hash % self.capacity
        bucket = self.data[index]

        for i, (k, v, h) in enumerate(bucket):
            if h == _hash:
                if k == key:
                    return v

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_data = [[] for _ in range(new_capacity)]

        for bucket in self.data:
            for key, value, _hash in bucket:
                new_index = _hash % new_capacity
                new_data[new_index].append((key, value, _hash))

        self.capacity = new_capacity
        self.data = new_data

    def clear(self) -> None:
        self.data = [[] for _ in range(self.capacity)]
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        _hash = hash(key)
        index = _hash % self.capacity
        bucket = self.data[index]

        for i, (k, v, h) in enumerate(bucket):
            if h == _hash:
                if k == key:
                    del bucket[i]
                    self.size -= 1
                    return
        raise KeyError(f"Key {key} not found")

    def update(
            self,
            other: dict | list[tuple] | None = None,
            **kwargs
    ) -> None:
        if other is not None:
            if isinstance(other, dict):
                items = other.items()
            else:
                items = other
            for key, value in items:
                self[key] = value

        for key, value in kwargs.items():
            self[key] = value

    def get(self, key: Any, default: Any = None) -> Any:
        _hash = hash(key)
        index = _hash % self.capacity
        bucket = self.data[index]

        for i, (k, v, h) in enumerate(bucket):
            if h == _hash:
                if k == key:
                    return v

        return default

    def pop(self, key: Any, default: Any = None) -> Any:
        _hash = hash(key)
        index = _hash % self.capacity
        bucket = self.data[index]

        for i, (k, v, h) in enumerate(bucket):
            if h == _hash:
                if k == key:
                    del bucket[i]
                    self.size -= 1
                    return v

        if default is not None:
            return default
        else:
            raise KeyError(f"Key {key} not found")

    def __iter__(self) -> Any:
        for bucket in self.data:
            for key, value, _hash in bucket:
                yield key
