from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.size = 0
        self.load_factor = 0.66
        self.tables = [[] for _ in range(self.capacity)]

    def _hash(self, key: Any) -> int:
        if not isinstance(key, Hashable):
            raise TypeError(f"unhashable type: {type(key)}")
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old_tables = self.tables
        self.capacity *= 2
        self.tables = [[] for _ in range(self.capacity)]
        self.size = 0

        for table in old_tables:
            for _key, _value in table:
                self[_key] = _value

    def __setitem__(self, key: Any, value: Any) -> Any:
        if self.size / self.capacity >= self.load_factor:
            self._resize()
        index = self._hash(key)

        tables = self.tables[index]

        for i, (_key, _) in enumerate(tables):
            if _key == key:
                tables[i] = (key, value)
                return

        tables.append((key, value))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        index = self._hash(key)
        tables = self.tables[index]

        for _key, _value in tables:
            if _key == key:
                return _value

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size

    def pop(self, key: Any, default: Any | None = None) -> Any | None:
        index = self._hash(key)
        table = self.tables[index]

        for i, (_key, _value) in enumerate(table):
            if _key == key:
                del table[i]
                return _value

        if default is not None:
            return default
        raise KeyError(f"Key '{key}' not found")
