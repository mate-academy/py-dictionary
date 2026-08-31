from typing import Any

_MISSING = object()


class Dictionary:
    def __init__(self) -> None:
        self.hash_table: list = [None] * 8
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        if len(self) + 1 > len(self.hash_table) * 2 / 3:
            self.__resize()
        self.__insert(key, value)

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % len(self.hash_table)
        while self.hash_table[index] is not None:
            if self.hash_table[index] == -2:
                index = (index + 1) % len(self.hash_table)
                continue
            node = self.hash_table[index]
            if node[1] == hash(key) and node[0] == key:
                return node[2]
            index = (index + 1) % len(self.hash_table)
        raise KeyError(key)

    def __resize(self) -> None:
        nodes = [node for node in self.hash_table if node and node != -2]
        self.hash_table = ([None] * (len(self.hash_table) * 2))
        self.length = 0
        for node in nodes:
            self.__insert(key=node[0], value=node[2])

    def __insert(self, key: Any, value: Any) -> None:
        hash_ = hash(key)
        index = hash_ % len(self.hash_table)
        while self.hash_table[index] and self.hash_table[index] != -2:
            node = self.hash_table[index]
            if node[1] == hash_ and node[0] == key:
                self.hash_table[index] = (key, hash_, value)
                return
            index = (index + 1) % len(self.hash_table)
        self.hash_table[index] = (key, hash_, value)
        self.length += 1

    def clear(self) -> None:
        self.hash_table = [None] * 8
        self.length = 0

    def __delitem__(self, key: Any) -> None:
        index = hash(key) % len(self.hash_table)
        while self.hash_table[index] is not None:
            if self.hash_table[index] == -2:
                index = (index + 1) % len(self.hash_table)
                continue
            node = self.hash_table[index]
            if node[1] == hash(key) and node[0] == key:
                self.hash_table[index] = -2
                self.length -= 1
                return
            index = (index + 1) % len(self.hash_table)
        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        index = hash(key) % len(self.hash_table)
        while self.hash_table[index] is not None:
            if self.hash_table[index] == -2:
                index = (index + 1) % len(self.hash_table)
                continue
            node = self.hash_table[index]
            if node[1] == hash(key) and node[0] == key:
                return node[2]
            index = (index + 1) % len(self.hash_table)
        return default

    def pop(self, key: Any, default: Any = _MISSING) -> Any:
        index = hash(key) % len(self.hash_table)
        while self.hash_table[index] is not None:
            if self.hash_table[index] == -2:
                index = (index + 1) % len(self.hash_table)
                continue
            node = self.hash_table[index]
            if node[1] == hash(key) and node[0] == key:
                value = node[2]
                self.hash_table[index] = -2
                self.length -= 1
                return value
            index = (index + 1) % len(self.hash_table)
        if default is not _MISSING:
            return default
        raise KeyError(key)

    def update(
        self, argument: dict | list[tuple[Any, Any]] = None, **kwargs
    ) -> None:
        if argument is not None:
            if isinstance(argument, dict):
                args = argument.items()
            elif isinstance(argument, list):
                args = argument
            else:
                raise TypeError(
                    "Argument must be a dict or list of key-value tuples"
                )
            for key, value in args:
                self.__setitem__(key, value)
        if kwargs:
            for key, value in kwargs.items():
                self.__setitem__(key, value)

    def __iter__(self) -> Any:
        for node in self.hash_table:
            if node is not None and node != -2:
                yield node[0]
