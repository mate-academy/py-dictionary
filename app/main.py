from typing import Any, Generator


class Dictionary:

    _DELETED = object()

    def __init__(self) -> None:
        self._length = 0
        self._table_size = 8
        self._threshold_factor = 2 / 3
        self._table: list = [None] * self._table_size

    @property
    def _threshold(self) -> int:
        return int(self._table_size * self._threshold_factor)

    def __len__(self) -> int:
        return self._length

    def __repr__(self) -> str:
        return str(self._table)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._length + 1 >= self._threshold:
            self._resize()
        self._insert(key, value)

    def __getitem__(self, key: Any) -> Any:
        index = self._find_key(key)
        if index is None:
            raise KeyError(f"Key not found: {key}")
        return self._table[index][1]

    def _resize(self) -> None:
        old_table = self._table
        self._table_size *= 2
        self._table: list = [None] * self._table_size
        self._length = 0

        for entry in old_table:
            if entry and entry is not self._DELETED:
                self._insert(*entry)

    def _insert(self, key: Any, value: Any) -> None:
        index = self._probe(key)
        if self._table[index] is None or self._table[index] is self._DELETED:
            self._length += 1
        self._table[index] = key, value

    def _find_key(self, key: Any) -> int | None:
        start_index = hash(key) % self._table_size
        for i in range(self._table_size):
            index = (start_index + i) % self._table_size
            entry = self._table[index]
            if entry is None:
                continue
            if (entry is not self._DELETED
                    and entry[0] == key and hash(entry[0]) == hash(key)):
                return index
        return None

    def _probe(self, key: Any) -> int:
        start_index = hash(key) % self._table_size
        for i in range(self._table_size):
            index = (start_index + i) % self._table_size
            entry = self._table[index]
            if (entry is None or entry is self._DELETED
                    or entry[0] == key and hash(entry[0]) == hash(key)):
                return index

        # Can't happen
        raise RuntimeError("Hash table is full")

    def clear(self) -> None:
        self._table = [None] * self._table_size
        self._length = 0

    def get(self, key: Any, default: Any = None) -> Any:
        index = self._find_key(key)
        if index is None:
            return default
        return self._table[index][1]

    def pop(self, key: Any, default: Any = ...) -> Any:
        index = self._find_key(key)
        if index is not None:
            value = self._table[index][1]
            self._table[index] = self._DELETED
            self._length -= 1
            return value
        elif default is not ...:
            return default
        else:
            raise KeyError(f"Key not found: {key}")

    def update(self, other: dict) -> None:
        if hasattr(other, "items"):
            for key, value in other.items():
                self[key] = value
        else:
            for key, value in other:
                self[key] = value

    def __delitem__(self, key: Any) -> None:
        index = self._find_key(key)
        if index is None:
            raise KeyError(f"Key not found: {key}")
        self._table[index] = self._DELETED
        self._length -= 1

    def __iter__(self) -> Any:
        for entry in self._table:
            if entry and entry is not self._DELETED:
                yield entry[0]

    def items(self) -> Generator:
        for entry in self._table:
            if entry and entry is not self._DELETED:
                yield entry

    def values(self) -> Generator:
        for entry in self._table:
            if entry and entry is not self._DELETED:
                yield entry[1]

    def keys(self) -> Generator:
        for entry in self._table:
            if entry and entry is not self._DELETED:
                yield entry[0]
