from __future__ import annotations

from typing import Any, Iterator, Hashable

_NOT_GIVEN = object()


class Dictionary:
    def __init__(self) -> None:
        self._length = 0
        self._hash_table: list = [None] * 8

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % len(self._hash_table)

        for _ in range(len(self._hash_table)):
            node = self._hash_table[index]

            if node is None:

                if (self._length + 1) * 3 >= len(self._hash_table) * 2:
                    self._resize()
                    self[key] = value
                    return

                self._hash_table[index] = (
                    key,
                    key_hash,
                    value
                )
                self._length += 1
                return

            if node[1] == key_hash and node[0] == key:
                self._hash_table[index] = (
                    key,
                    key_hash,
                    value
                )
                return

            index = (index + 1) % len(self._hash_table)

    def _resize(self) -> None:
        old_hash_table = self._hash_table
        self._hash_table = [None] * (len(old_hash_table) * 2)
        self._length = 0

        for node in old_hash_table:
            if node is not None:
                key, _, value = node
                self[key] = value

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % len(self._hash_table)

        for _ in range(len(self._hash_table)):
            node = self._hash_table[index]

            if node is None:
                raise KeyError(key)

            if node[0] == key and node[1] == key_hash:
                return node[2]

            index = (index + 1) % len(self._hash_table)

        raise KeyError(key)

    def __len__(self) -> int:
        return self._length

    def clear(self) -> None:
        self._length = 0
        self._hash_table = [None] * 8

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = key_hash % len(self._hash_table)

        for _ in range(len(self._hash_table)):
            node = self._hash_table[index]

            if node is None:
                raise KeyError(key)

            if node[0] == key and node[1] == key_hash:
                self._hash_table[index] = None
                self._length -= 1

                index = (index + 1) % len(self._hash_table)

                while self._hash_table[index] is not None:
                    node_key, _, node_value = self._hash_table[index]

                    self._hash_table[index] = None
                    self._length -= 1

                    self[node_key] = node_value

                    index = (index + 1) % len(self._hash_table)

                return

            index = (index + 1) % len(self._hash_table)

        raise KeyError(key)

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = _NOT_GIVEN) -> Any:
        key_hash = hash(key)
        index = key_hash % len(self._hash_table)

        for _ in range(len(self._hash_table)):
            node = self._hash_table[index]

            if node is None:
                if default is _NOT_GIVEN:
                    raise KeyError(key)

            if node[0] == key and node[1] == key_hash:
                value = node[2]

                del self[key]

                return value

            index = (index + 1) % len(self._hash_table)

        if default is _NOT_GIVEN:
            raise KeyError(key)

        return default

    def update(self, other: Dictionary) -> None:
        for node in other._hash_table:
            if node is not None:
                key, _, value = node
                self[key] = value

    def __iter__(self) -> Iterator[Any]:
        for node in self._hash_table:
            if node is not None:
                yield node[0]
