from dataclasses import dataclass
from typing import Hashable, Any
from typing import Callable


@dataclass
class Node:
    key: Hashable
    hash_: int
    value: Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3
    CAPACITY_MULTIPLIER = 2

    def __init__(self, capacity: int = INITIAL_CAPACITY,
                 hash_function: Callable[[Hashable], int] = hash) -> None:
        self.capacity = capacity
        self.length = 0
        self._hash_table: list[None | Node] = [None] * capacity
        self.hash_function = hash_function

    @property
    def _table_limit(self) -> int:
        return self.LOAD_FACTOR * self.capacity

    def _get_index(self, key: Hashable) -> int:
        hash_ = self.hash_function(key)
        index = hash_ % self.capacity

        while (
                self._hash_table[index] is not None
                and self._hash_table[index].hash_ != key
                and self._hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity

        return index

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        self.__init__(self.capacity * self.CAPACITY_MULTIPLIER)

        for element in old_hash_table:
            if element:
                self[element.key] = element.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            if self.length + 1 >= self._table_limit:
                self._resize()
                self[key] = value
            else:
                self._hash_table[index] = Node(key, hash(key), value)
                self.length += 1
        else:
            self._hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            raise KeyError(f"No such key: {key}")

        return self._hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)

        if self._hash_table.get(index) is None:
            raise KeyError(f"No such key: {key}")

        self._hash_table[index] = None
        self.length -= 1

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: Hashable) -> bool:
        index = self._get_index(key)

        return self._hash_table[index] is not None

    def __len__(self) -> int:
        return self.length

    def pop(self, *args) -> Any:
        key, *other = args

        if key in self:
            value = self[key]
            del self[key]

            return value

        if len(other) == 0:
            raise KeyError("No such key")
        elif len(other) > 1:
            raise TypeError(f"pop expected at most 2 arguments, "
                            f"got {len(args)}")
        return other[0]
