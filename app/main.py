from typing import Any, Iterable, Mapping, Tuple


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 0.75,
                 ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def hash_key(self, key: int) -> int:
        return hash(key) % self.capacity

    def __setitem__(self,
                    key: int | str | float | tuple | bool,
                    value: Any
                    ) -> None:
        hash_key = self.hash_key(key)
        bucket = self.table[hash_key]
        for index, (k, _) in enumerate(bucket):
            if k == key:
                bucket[index] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size / self.capacity > self.load_factor:
            self.resize()

    def __getitem__(self,
                    key: int | str | float | tuple | bool,
                    ) -> Any:
        hash_key = self.hash_key(key)
        bucket = self.table[hash_key]

        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def __delitem__(self,
                    key: int | str | float | tuple | bool,
                    ) -> None:
        hash_key = self.hash_key(key)
        bucket = self.table[hash_key]

        for idx, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[idx]
                self.size -= 1
                return

        raise KeyError(f"Key '{key}' not found")

    def __iter__(self) -> Iterable:
        for bucket in self.table:
            for key, value in bucket:
                yield key

    def get(self,
            key: int | str | float | tuple | bool,
            default: Any = None
            ) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self.capacity = 8
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for key, value in bucket:
                self[key] = value

    def pop(self,
            key: int | str | float | tuple | bool,
            default: Any = None
            ) -> Any:
        hash_key = self.hash_key(key)
        bucket = self.table[hash_key]

        for idx, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[idx]
                self.size -= 1
                return v

        if default is not None:
            return default
        raise KeyError(f"Key '{key}' not found")

    def update(self,
               other: Mapping | Iterable[Tuple[Any, Any]] = None,
               ) -> None:
        for key, value in other.items():
            self[key] = value
