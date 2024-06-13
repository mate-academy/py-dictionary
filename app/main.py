from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    hash_: int
    value: Any


class Dictionary:
    LOAD_FACTOR = 2 / 3
    DEFAULT_CAPACITY = 8

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        self.capacity = capacity
        self.length = 0
        self._hash_table = [None] * self.capacity

    def check_max_load(self) -> float:
        return self.capacity * self.LOAD_FACTOR

    def _get_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self.capacity

        while (self._hash_table[index] is not None
               and self._hash_table[index].key != key):
            index += 1
            index = index % self.capacity

        return index

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        self.__init__(self.capacity * 2)

        for node in old_hash_table:
            if node:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if self.length + 1 >= self.check_max_load():
            self._resize()
            index = self._get_index(key)
            if self._hash_table[index] is None:
                self.length += 1
            self._hash_table[index] = Node(key, hash(key), value)
            return

        index = self._get_index(key)
        if self._hash_table[index] is None:
            self.length += 1
        self._hash_table[index] = Node(key, hash(key), value)

    def __getitem__(self, key: Hashable) -> Any | KeyError:
        index = self._get_index(key)
        if self._hash_table[index] is None:
            raise KeyError("Key not found")
        return self._hash_table[index].value

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        if self._hash_table[index] is None:
            raise KeyError("Key not found")
        self._hash_table[index] = None
        self.length -= 1

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Hashable, default: Any = None) -> Any | None:
        try:
            self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, *args) -> Any:
        key, *other = args

        if key in self:
            value = self[key]
            del self[key]

            return value

        if len(other) == 0:
            raise KeyError("No such key")
        elif len(other) > 1:
            raise TypeError(
                f"pop expected at most 2 arguments, got {len(args)}"
            )
        return other[0]
