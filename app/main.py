from typing import Hashable, Any, Iterable, Iterator


class Node:
    def __init__(self, key: Hashable, hash_: int, value: Any) -> None:
        self.key = key
        self.hash = hash_
        self.value = value


class Dictionary(Iterable):
    _DEFAULT_CAPACITY = 8
    _LOAD_FACTOR = 2 / 3
    _CAPACITY_MULTIPLIER = 2

    def __init__(self, capacity: int = _DEFAULT_CAPACITY) -> None:
        self._capacity = capacity
        self._length = 0
        self._hash_table: list[None | Node] = [None] * capacity

    def _table_limit(self) -> int:
        return int(self._LOAD_FACTOR * self._capacity)

    def _get_index(self, key: Hashable) -> int:
        hash_ = hash(key)
        index = hash_ % self._capacity

        while (
                self._hash_table[index] is not None
                and self._hash_table[index].key != key
        ):
            index = (index + 1) % self._capacity

        return index

    def _resize(self) -> None:
        hash_table = self._hash_table
        self.__init__(self._capacity * self._CAPACITY_MULTIPLIER)

        for element in hash_table:
            if element:
                self[element.key] = element.value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            if self._length + 1 >= self._table_limit():
                self._resize()
                self[key] = value
            else:
                self._hash_table[index] = Node(key, hash(key), value)
                self._length += 1
        else:
            self._hash_table[index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            raise KeyError(f"No such key: {key}")

        return self._hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self._get_index(key)

        if self._hash_table[index] is None:
            raise KeyError(f"No such key: {key}")

        self._hash_table[index] = None
        self._length -= 1

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
        return self._length

    def pop(self, *args) -> Any:
        key, *other = args

        if key in self:
            value = self[key]
            del self[key]

            return value

        if len(other) == 0:
            raise KeyError("No such key")
        if len(other) > 1:
            raise TypeError(
                f"pop expected at most 2 arguments, got {len(args)}"
            )
        return other[0]

    def update(self, iterable: Iterable[Any] | dict[Any]) -> None:
        if hasattr(iterable, "keys"):
            for key in iterable:
                self[key] = iterable[key]
        else:
            for key, value in iterable:
                self[key] = value

    def __iter__(self) -> "DictionaryIterator":
        return DictionaryIterator(self._hash_table)


class DictionaryIterator(Iterator):
    def __init__(self, items: list[Any]) -> None:
        self._items = items
        self._index = 0

    def __iter__(self) -> "DictionaryIterator":
        self._index = 0
        return self

    def __next__(self) -> Any:
        while (
                self._index < len(self._items)
                and self._items[self._index] is None
        ):
            self._index += 1

        if self._index >= len(self._items):
            raise StopIteration

        key = self._items[self._index].key
        self._index += 1
        return key
