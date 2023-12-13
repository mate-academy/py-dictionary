from typing import Mapping, Any, Hashable


class Dictionary(Mapping):
    def __init__(self, capacity: int = 8, load_factor: float = 0.75) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.count = 0
        self.table = [None] * self.capacity

    def __iter__(self) -> Any:
        for item in self.table:
            if item is not None:
                yield item[0]

    def __len__(self) -> int:
        return self.count

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.count / self.capacity >= self.load_factor:
            self._resize()

        index = self._hash(key) % self.capacity
        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.capacity

        if self.table[index] is None:
            self.count += 1
            self.table[index] = (key, self._hash(key), value)
        else:
            self.table[index] = (key, self.table[index][1], value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_key(key)
        if index is None:
            raise KeyError(key)
        else:
            return self.table[index][2]

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: object = None, default: Any = None) -> Any:
        if key is None and default is None:
            raise KeyError(
                "Either existing key or default value should be provided"
            )

        index = self._find_key(key)
        if index is None:
            return default
        else:
            value = self.table[index][2]
            self.table[index] = None
            self.count -= 1
            return value

    def update(self, *args, **kwargs) -> None:
        if args:
            other = args[0]
            if isinstance(other, Mapping | Dictionary):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value
        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def _find_key(self, key: Hashable) -> int:
        index = self._hash(key) % self.capacity
        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.capacity
        return index if self.table[index] is not None else None

    def _resize(self) -> None:
        self.capacity *= 2
        new_table = [None] * self.capacity
        for item in self.table:
            if item is not None:
                index = item[1] % self.capacity
                while (
                    new_table[index] is not None
                    and new_table[index][0] != item[0]
                ):
                    index = (index + 1) % self.capacity
                new_table[index] = item
        self.table = new_table

    def _hash(self, key: Hashable) -> int:
        return hash(key)

    def items(self) -> list:
        return [(node[0], node[2]) for node in self.table if node is not None]

    def clear(self) -> None:
        self.table.clear()
        self.count = 0
