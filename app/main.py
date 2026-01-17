from __future__ import annotations


class Dictionary:
    def __init__(self,
                 initial_capacity: int = 8,
                 load_factor: float = 0.66
                 ) -> None:
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.load_factor: float = load_factor
        self.table: list[tuple | None | object] = [None] * self.capacity
        self.dummy: object = object()

    def _find_slot(self, key: object, insert: bool = False) -> int | None:
        original_index = hash(key) % self.capacity
        index = original_index
        first_dummy = None

        while True:
            if self.table[index] is None:
                return (
                    first_dummy if (first_dummy is not None and insert)
                    else index
                )
            elif self.table[index] is self.dummy:
                if first_dummy is None:
                    first_dummy = index
            elif self.table[index][0] == key:
                return index

            index = (index + 1) % self.capacity
            if index == original_index:
                if insert:
                    self._resize()
                    return self._find_slot(key, insert=True)
                return None

    def __setitem__(self, key: object, value: object) -> None:
        if self.size + 1 > self.capacity * self.load_factor:
            self._resize()
        index = self._find_slot(key, insert=True)
        if self.table[index] is None or self.table[index] is self.dummy:
            self.size += 1
        self.table[index] = (key, value)

    def __getitem__(self, key: object) -> object:
        index = self._find_slot(key)
        if index is None or self.table[index] is None:
            raise KeyError(f"Key '{key}' not found")
        return self.table[index][1]

    def __delitem__(self, key: object) -> None:
        index = self._find_slot(key)
        if index is None:
            raise KeyError(f"Key '{key}' not found")
        self.table[index] = self.dummy
        self.size -= 1

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> iter:
        for entry in self.table:
            if entry is not None and entry is not self.dummy:
                yield entry[0]

    def keys(self) -> iter:
        for entry in self.table:
            if entry is not None and entry is not self.dummy:
                yield entry[0]

    def values(self) -> iter:
        for entry in self.table:
            if entry is not None and entry is not self.dummy:
                yield entry[1]

    def items(self) -> iter:
        for entry in self.table:
            if entry is not None and entry is not self.dummy:
                yield entry[0], entry[1]

    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def get(self, key: object, default: object = None) -> object:
        index = self._find_slot(key)
        return self.table[index][1] if index is not None else default

    def pop(self, key: object, default: object = None) -> object:
        index = self._find_slot(key)
        if index is None:
            if default is None:
                raise KeyError(f"Key '{key}' not found")
            return default
        value = self.table[index][1]
        self.table[index] = self.dummy
        self.size -= 1
        return value

    def update(self, other: Dictionary) -> None:
        if not isinstance(other, Dictionary):
            raise TypeError("Argument must be an instance of Dictionary")
        for key, value in other.items():
            self[key] = value

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for entry in old_table:
            if entry is not None and entry is not self.dummy:
                self.__setitem__(entry[0], entry[1])
