from collections.abc import Iterator, Mapping, Iterable
from typing import Generic, TypeVar, Any

K = TypeVar("K")
V = TypeVar("V")
D = TypeVar("D")

DELETED = object()
MISSING = object()


class Dictionary(Generic[K, V]):

    def __init__(self) -> None:
        self.capacity: int = 8
        self.max_load_factor: float = 2 / 3
        self.length: int = 0
        self.hash_table: list[Any] \
            = [None] * self.capacity

    def __setitem__(self, key: K, value: V) -> None:
        hash_value = hash(key)
        index = self._find_slot(key, hash_value)

        if (
                index is not None
                and self.hash_table[index] is not DELETED
                and self.hash_table[index] is not None
                and self.hash_table[index][0] == key
        ):
            self.hash_table[index][2] = value
            return

        if (
                index is None
                or (self.length + 1) / self.capacity >= self.max_load_factor
        ):
            self._resize()
            index = self._find_slot(key, hash_value)

        self.hash_table[index] = [key, hash_value, value]
        self.length += 1

    def __getitem__(self, key: K) -> V:
        hash_value = hash(key)
        index = self._find_slot(key, hash_value)
        if (
                index is not None
                and self.hash_table[index] is not DELETED
                and self.hash_table[index] is not None
                and self.hash_table[index][1] == hash_value
                and self.hash_table[index][0] == key
        ):
            return self.hash_table[index][2]
        else:
            raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: K) -> None:
        hash_value = hash(key)
        index = self._find_slot(key, hash_value)
        if (
                index is None
                or self.hash_table[index] is DELETED
                or self.hash_table[index] is None
        ):
            raise KeyError(key)

        self.hash_table[index] = DELETED
        self.length -= 1

    def __iter__(self) -> Iterator[K]:
        for value in self.hash_table:
            if value is not None and value is not DELETED:
                yield value[0]

    def get(self, key: K, default: D = None) -> V | D | None:
        hash_value = hash(key)
        index = self._find_slot(key, hash_value)
        if (
                index is None
                or self.hash_table[index] is DELETED
                or self.hash_table[index] is None
        ):
            return default
        elif self.hash_table[index][0] != key:
            return default
        else:
            return self.hash_table[index][2]

    def clear(self) -> None:
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity
        self.length = 0

    def pop(self, key: K, default: D = MISSING) -> V | D:
        try:
            deleted_element = self.__getitem__(key)
            self.__delitem__(key)
            return deleted_element
        except KeyError:
            if default is not MISSING:
                return default
            else:
                raise

    def update(
            self,
            other: Mapping[K, V] | Iterable[tuple[K, V]] = None,
            **kwargs
    ) -> None:
        if isinstance(other, Mapping):
            other = other.items()

        if other is not None:
            for key, value in other:
                self.__setitem__(key, value)

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def _find_slot(self, key: K, hash_value: int) -> int | None:
        start_index = hash_value % len(self.hash_table)
        index = start_index
        deleted_index = None

        while True:
            if self.hash_table[index] is DELETED:
                if deleted_index is None:
                    deleted_index = index
            elif self.hash_table[index] is None:
                return deleted_index if deleted_index is not None else index
            elif (
                    self.hash_table[index][1] == hash_value
                    and self.hash_table[index][0] == key
            ):
                return index

            index = (index + 1) % len(self.hash_table)

            if index == start_index:
                return deleted_index if deleted_index is not None else None

    def _resize(self) -> None:
        old_hash_table = self.hash_table
        self.hash_table = [None] * (2 * self.capacity)
        self.capacity *= 2
        self.length = 0

        for item in old_hash_table:
            if item is DELETED or item is None:
                continue
            else:
                index = self._find_slot(item[0], item[1])
                self.hash_table[index] = item
                self.length += 1
