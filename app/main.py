from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.table: list = [None] * capacity
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        h = hash(key)
        index = h % self.capacity

        if self.table[index] is None:
            self.table[index] = [(key, h, value)]
            self.size += 1
            return

        for i, (k, stored_hash, v) in enumerate(self.table[index]):
            if stored_hash == h and k == key:
                self.table[index][i] = (key, h, value)
                return

        self.table[index].append((key, h, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        index = h % self.capacity

        if self.table[index] is None:
            raise KeyError(f"Key not found: {key!r}")

        for k, stored_hash, v in self.table[index]:
            if stored_hash == h and k == key:
                return v

        raise KeyError(f"Key not found: {key!r}")

    def __len__(self) -> int:
        return self.size

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        h = hash(key)
        index = h % self.capacity

        if self.table[index] is None:
            raise KeyError(f"Key not found: {key!r}")

        for i, (k, stored_hash, v) in enumerate(self.table[index]):
            if stored_hash == h and k == key:
                del self.table[index][i]
                self.size -= 1

                if not self.table[index]:
                    self.table[index] = None
                return

        raise KeyError(f"Key not found: {key!r}")

    def pop(self, key: Any, default: Any = None) -> Any:
        h = hash(key)
        index = h % self.capacity

        if self.table[index] is None:
            if default is not None:
                return default
            raise KeyError(f"Key not found: {key!r}")

        for i, (k, stored_hash, v) in enumerate(self.table[index]):
            if stored_hash == h and k == key:
                value = v
                del self.table[index][i]
                self.size -= 1

                if not self.table[index]:
                    self.table[index] = None

                return value

        if default is not None:
            return default

        raise KeyError(f"Key not found: {key!r}")

    def update(self, other: Any) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> None:
        for bucket in self.table:
            if bucket is not None:
                for key, _, _ in bucket:
                    yield key
