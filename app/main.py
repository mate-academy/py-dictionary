from typing import Any, Hashable, Iterator


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 0.67
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size / self.capacity >= self.load_factor:
            self._resize()
        index = hash(key) % self.capacity
        if self.table[index] is None:
            self.table[index] = []
        for i, (h, k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (hash(key), key, value)
                return
        self.table[index].append((hash(key), key, value))
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            for h, k, v in self.table[index]:
                if k == key:
                    return v
        raise KeyError(f"Key {key} not found")

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            for i, (h, k, v) in enumerate(self.table[index]):
                if k == key:
                    del self.table[index][i]
                    self.size -= 1
                    return

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise

    def update(self, other: dict[Hashable, Any]) -> None:
        for key, value in other.items():
            self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for slot in self.table:
            if slot is not None:
                for h, k, v in slot:
                    yield k

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for slot in self.table:
            if slot is not None:
                for h, k, v in slot:
                    new_index: int = h % new_capacity
                    if new_table[new_index] is None:
                        new_table[new_index] = []
                    new_table[new_index].append((h, k, v))
        self.table = new_table
        self.capacity = new_capacity
