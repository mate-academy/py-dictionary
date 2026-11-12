from __future__ import annotations

from collections.abc import Iterator


class Node:
    def __init__(self, key: object, hash_value: int, value: object) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class _Tombstone:
    pass


_TOMBSTONE = _Tombstone()


class Dictionary:
    def __init__(
        self,
        capacity: int = 8,
        load_factor: float = 0.75,
    ) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be greater than zero")

        if not 0 < load_factor < 1:
            raise ValueError(
                "load_factor must be greater than zero and less than one"
            )

        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.hash_table: list[Node | _Tombstone | None] = [None] * capacity

    def __setitem__(self, key: object, value: object) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity
        first_deleted: int | None = None

        for _ in range(self.capacity):
            node = self.hash_table[index]

            if node is None:
                target_index = (
                    first_deleted if first_deleted is not None else index
                )
                self.hash_table[target_index] = Node(
                    key,
                    hash_value,
                    value,
                )
                self.size += 1

                if self.size / self.capacity > self.load_factor:
                    self._resize()

                return

            if isinstance(node, _Tombstone):
                if first_deleted is None:
                    first_deleted = index
            elif node.hash == hash_value and node.key == key:
                node.value = value
                return

            index = (index + 1) % self.capacity

        if first_deleted is not None:
            self.hash_table[first_deleted] = Node(key, hash_value, value)
            self.size += 1
            return

        self._resize()
        self[key] = value

    def __getitem__(self, key: object) -> object:
        hash_value = hash(key)
        index = hash_value % self.capacity

        for _ in range(self.capacity):
            node = self.hash_table[index]

            if node is None:
                break

            if not isinstance(node, _Tombstone):
                if node.hash == hash_value and node.key == key:
                    return node.value

            index = (index + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: object) -> bool:
        try:
            self.__getitem__(key)
        except KeyError:
            return False

        return True

    def __iter__(self) -> Iterator[object]:
        for node in self.hash_table:
            if node is not None and not isinstance(node, _Tombstone):
                yield node.key

    def __delitem__(self, key: object) -> None:
        hash_value = hash(key)
        index = hash_value % self.capacity

        for _ in range(self.capacity):
            node = self.hash_table[index]

            if node is None:
                break

            if not isinstance(node, _Tombstone):
                if node.hash == hash_value and node.key == key:
                    self.hash_table[index] = _TOMBSTONE
                    self.size -= 1
                    return

            index = (index + 1) % self.capacity

        raise KeyError(key)

    def get(self, key: object, default: object = None) -> object:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: object, *args: object) -> object:
        if len(args) > 1:
            raise TypeError(
                "pop expected at most 2 arguments, got "
                f"{len(args) + 1}"
            )

        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
        except KeyError:
            if args:
                return args[0]

            raise

        return value

    def update(self, other: object) -> None:
        if isinstance(other, Dictionary):
            for key in other:
                self[key] = other[key]

            return

        for key, value in other:
            self[key] = value

    def clear(self) -> None:
        self.size = 0
        self.hash_table = [None] * self.capacity

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for node in old_table:
            if node is None or isinstance(node, _Tombstone):
                continue

            index = node.hash % self.capacity

            while self.hash_table[index] is not None:
                index = (index + 1) % self.capacity

            self.hash_table[index] = node
            self.size += 1
