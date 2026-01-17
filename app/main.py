from dataclasses import dataclass
from typing import Hashable, Any


@dataclass
class Node:
    key: Hashable
    hash_value: int
    value: Any
    is_deleted: bool = False


class Dictionary:
    LOAD_FACTOR = 2 / 3
    CAPACITY_MULTIPLIER = 2
    INITIAL_CAPACITY = 8

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        self.capacity = capacity
        self._size = 0
        self._hash_table: list[None | Node] = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._calculate_index(key)
        if ((node := self._hash_table[index]) is not None
                and not node.is_deleted):
            node.value = value
            return
        self._hash_table[index] = Node(
            key=key,
            hash_value=hash(key),
            value=value
        )
        self._size += 1
        self._check_resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._calculate_index(key)
        if not (node := self._hash_table[index]) or node.is_deleted:
            raise KeyError
        return node.value

    def __delitem__(self, key: Hashable) -> None:
        index = self._calculate_index(key)
        if not (node := self._hash_table[index]) or node.is_deleted:
            raise KeyError
        node.is_deleted = True
        self._size -= 1

    def pop(self, *args) -> Any:
        if len(args) > 2:
            raise TypeError(f"pop expected at most 2 arguments, got "
                            f"{len(args)}")

        key, *default = args

        try:
            value = self[key]  # self.__getitem__(key)
            del self[key]

            return value
        except KeyError:
            if not default:
                raise

            return default[0]

    def _resize(self) -> None:
        current_hash_table = self._hash_table
        self.capacity = self.capacity * self.CAPACITY_MULTIPLIER
        self._hash_table = [None] * self.capacity
        self._size = 0
        for node in current_hash_table:
            if node and not node.is_deleted:
                self[node.key] = node.value

    def _check_resize(self) -> None:
        if self._size > self._max_size:
            self._resize()

    @property
    def _max_size(self) -> float:
        return self.capacity * self.LOAD_FACTOR

    def _linear_probing(self, index: int) -> int:
        return (index + 1) % self.capacity

    def _calculate_index(self, key: Hashable) -> int:
        hash_value = hash(key)
        index = hash_value % self.capacity
        first_deleted = None
        while (node := self._hash_table[index]) and node.key != key:
            index = self._linear_probing(index)
            if node.is_deleted and first_deleted is None:
                first_deleted = index
        if node is None and first_deleted:
            index = first_deleted
        return index

    def __len__(self) -> int:
        return self._size
