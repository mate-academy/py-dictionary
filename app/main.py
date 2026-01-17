from dataclasses import dataclass
from typing import Hashable, Any, Optional


@dataclass
class Node:
    key: Hashable
    value: Any


class Dictionary:

    """sets the initial size of the dictionary."""
    INITIAL_CAPACITY = 8

    """value for increase size of dictionary."""
    RESIZE_THRESHOLD = 2 / 3

    """the size by which the dictionary capacity grows"""
    CAPACITY_MULTIPLIER = 2

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self.hash_table: list[Node | None] = [None] * self.capacity
        self.size = 0

    def dict_max_size(self) -> float:
        return self.RESIZE_THRESHOLD * self.capacity

    def _get_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while self.hash_table[index] and self.hash_table[index].key != key:
            index = self._increment_collision(index)
        return index

    def _increment_collision(self, index: int) -> int:
        return (index + 1) % self.capacity

    def resize(self) -> None:
        saved_hash_table = self.hash_table
        self.__init__(self.capacity * 2)

        for node in saved_hash_table:
            if node:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)

        if not self.hash_table[index]:
            if self.size + 1 >= self.dict_max_size():
                self.resize()
                index = self._get_index(key)
            self.size += 1
        self.hash_table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)
        if not self.hash_table[index]:
            raise KeyError(key)
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.size = 0

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)
        if not self.hash_table[index]:
            raise KeyError(key)
        self.hash_table[index] = None
        self.size -= 1

    def get(
            self,
            key: Hashable,
            default: Optional[Any] = None
    ) -> Optional[Any]:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Optional[Any] = None) -> Any:
        try:
            value = self.get(key)
            self.__delitem__(key)
            return value
        except KeyError:
            if default:
                return default
            else:
                raise

    def update(self, other_dict: dict) -> None:
        if isinstance(other_dict, dict):
            for key, value in other_dict.items():
                self.__setitem__(key, value)
        else:
            for key, value in other_dict:
                self.__setitem__(key, value)

    def __iter__(self) -> None:
        for node in self.hash_table:
            if node:
                yield node.key
