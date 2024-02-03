from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self._size = 8
        self._len = 0
        self._total_amount = 0
        self._hash_table = [None] * self._size

    def _index(self, key: Hashable) -> int:
        return hash(key) % self._size

    def _resize(self) -> None:
        self._size *= 2
        self._total_amount = self._len
        new_hash_table = [None] * self._size

        for node in self._hash_table:
            if isinstance(node, tuple):
                index = self._index(node[0])
                while new_hash_table[index]:
                    index = (index + 1) % self._size
                new_hash_table[index] = node

        self._hash_table = new_hash_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._index(key)

        while self._hash_table[index]:
            if (
                isinstance(self._hash_table[index], tuple)
                and self._hash_table[index][0] == key
            ):
                self._hash_table[index] = (key, hash(key), value)
                return
            index = (index + 1) % self._size

        self._hash_table[index] = (key, hash(key), value)
        self._len += 1
        self._total_amount += 1

        if self._total_amount > int(self._size * 2 / 3):
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._index(key)

        while self._hash_table[index]:
            if (
                isinstance(self._hash_table[index], tuple)
                and self._hash_table[index][0] == key
            ):
                return self._hash_table[index][2]
            index = (index + 1) % self._size

        raise KeyError("No such key exists")

    def __len__(self) -> int:
        return self._len

    def __delitem__(self, key: Hashable) -> None:
        index = self._index(key)
        while self._hash_table[index]:
            if (
                isinstance(self._hash_table[index], tuple)
                and self._hash_table[index][0] == key
            ):
                self._hash_table[index] = "Deleted"
                self._len -= 1
                return
            index = (index + 1) % self._size
        raise KeyError("No such key exists")

    def clear(self) -> None:
        self.__init__()

    def get(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default_value

    def pop(self, key: Hashable, default_value: Any = None) -> Any:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default_value is not None:
                return default_value
            raise

    def __iter__(self) -> iter:
        for node in self._hash_table:
            if isinstance(node, tuple):
                yield node[0]

    def update(self, other: dict) -> None:
        for key, value in other.items():
            self[key] = value
