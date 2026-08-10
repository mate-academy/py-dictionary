from typing import Any


class _Node:
    __slots__ = ("key", "hash", "value")

    def __init__(self, key: Any, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class _Tombstone:
    pass


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self._capacity = max(1, initial_capacity)
        self._size = 0
        self._table = [None] * self._capacity
        self._load_factor = 0.66

    def __setitem__(self, key: Any, value: Any) -> None:
        if self._should_resize():
            self._resize()

        hash_value = hash(key)
        index, found, tombstone_index = self._find_slot(
            hash_value,
            key,
            for_insert=True,
        )

        if found:
            self._table[index].value = value
            return

        insert_index = (
            tombstone_index if tombstone_index is not None else index
        )
        self._table[insert_index] = _Node(key, hash_value, value)
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value = hash(key)
        index, found, _ = self._find_slot(hash_value, key)

        if not found:
            raise KeyError(
                key,
            )

        return self._table[index].value

    def __delitem__(self, key: Any) -> None:
        hash_value = hash(key)
        index, found, _ = self._find_slot(hash_value, key)

        if not found:
            raise KeyError(key)

        self._table[index] = _Tombstone()
        self._size -= 1

    def __len__(self) -> int:
        return self._size

    def _should_resize(self) -> bool:
        return (self._size + 1) / self._capacity >= self._load_factor

    def _resize(self) -> None:
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0

        for node in old_table:
            if node is not None:
                self._set_from_node(node)

    def _set_from_node(self, node: _Node) -> None:
        index, found, _ = self._find_slot(
            node.hash,
            node.key,
            for_insert=True,
        )
        if found:
            self._table[index].value = node.value
            return

        insert_index = index
        self._table[insert_index] = _Node(node.key, node.hash, node.value)
        self._size += 1

    def _find_slot(
        self,
        hash_value: int,
        key: Any,
        for_insert: bool = False,
    ) -> tuple[int, bool, int | None]:
        index = hash_value % self._capacity
        start_index = index
        first_tombstone = None

        while True:
            node = self._table[index]
            if node is None:
                return index, False, first_tombstone if for_insert else None

            if isinstance(node, _Tombstone):
                if first_tombstone is None:
                    first_tombstone = index
            elif node.hash == hash_value and node.key == key:
                return index, True, first_tombstone if for_insert else None

            index = (index + 1) % self._capacity
            if index == start_index:
                raise RuntimeError("Dictionary is full")
