from dataclasses import dataclass
from typing import Any, Hashable


@dataclass
class Node:
    key_hash: int
    key: Hashable
    value: Any


class Dictionary:
    CAPACITY_MULTIPLIER = 2

    def __init__(self, size: int = 8, load_factor: float = 0.66) -> None:
        self.size = size
        self.hash_table = [None] * size
        self.length = 0
        self.load_factor = load_factor

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._check_resize()
        index = self._get_index(key)

        if self.hash_table[index]:
            self.hash_table[index].value = value
        else:
            self.hash_table[index] = Node(hash(key), key, value)
            self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)

        if not self.hash_table[index]:
            raise KeyError(f"There is not key: {key}")

        return self.hash_table[index].value

    def __contains__(self, key: Hashable) -> bool:
        index = self._get_index(key)
        return self.hash_table[index] is not None

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        if self.hash_table[index]:
            self.hash_table[index] = None
            self.length -= 1
        else:
            raise KeyError(f"There is not key: {key}")

    @property
    def _check_limit(self) -> bool:
        return self.length / self.size >= self.load_factor

    def _check_resize(self) -> None:
        if self._check_limit:
            self._resize()

    def _get_index(self, key: Hashable) -> int:
        index = hash(key) % self.size
        end_index = index - 1
        while end_index != index:
            exists = (self.hash_table[index]
                      and self.hash_table[index].key == key)
            if exists or not self.hash_table[index]:
                return index
            index = (index + 1) % self.size

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.__init__(self.CAPACITY_MULTIPLIER * self.size)

        for node in old_hash_table:
            if node:
                self[node.key] = node.value

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
