from builtins import hash
from typing import Any


class Node:
    def __init__(
        self,
        key: Any,
        value: Any,
        hash_value: int,
    ) -> None:
        self.key = key
        self.value = value
        self.hash = hash_value


class Dictionary:
    def __init__(
        self,
        initial_capacity: int = 8,
        load_factor: float = 0.7,
    ) -> None:
        if initial_capacity <= 0:
            raise ValueError("initial_capacity должен быть больше 0")

        if not 0 < load_factor < 1:
            raise ValueError("load_factor должен быть между 0 и 1")

        self._capacity = initial_capacity
        self._load_factor = load_factor
        self._size = 0
        self._buckets: list[Node | None] = [None] * self._capacity

    def __len__(self) -> int:
        return self._size

    def _get_hash(self, key: Any) -> int:
        return hash(key)

    def _get_index(self, hash_value: int) -> int:
        return hash_value % self._capacity

    def _resize(self) -> None:
        old_buckets = self._buckets

        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0

        for node in old_buckets:
            if node is not None:
                self[node.key] = node.value

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_value = self._get_hash(key)
        index = self._get_index(hash_value)
        start_index = index

        while self._buckets[index] is not None:
            node = self._buckets[index]

            if node.hash == hash_value and node.key == key:
                node.value = value
                return

            index = (index + 1) % self._capacity

            if index == start_index:
                break

        if (self._size + 1) / self._capacity > self._load_factor:
            self._resize()
            index = self._get_index(hash_value)

            while self._buckets[index] is not None:
                index = (index + 1) % self._capacity
        else:
            while self._buckets[index] is not None:
                index = (index + 1) % self._capacity

        self._buckets[index] = Node(key, value, hash_value)
        self._size += 1

    def __getitem__(self, key: Any) -> Any:
        hash_value = self._get_hash(key)
        index = self._get_index(hash_value)
        start_index = index

        while self._buckets[index] is not None:
            node = self._buckets[index]

            if node.hash == hash_value and node.key == key:
                return node.value

            index = (index + 1) % self._capacity

            if index == start_index:
                break

        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        hash_value = self._get_hash(key)
        index = self._get_index(hash_value)
        start_index = index

        while self._buckets[index] is not None:
            node = self._buckets[index]

            if node.hash == hash_value and node.key == key:
                break

            index = (index + 1) % self._capacity

            if index == start_index:
                raise KeyError(key)
        else:
            raise KeyError(key)

        self._buckets[index] = None
        self._size -= 1

        next_index = (index + 1) % self._capacity

        while self._buckets[next_index] is not None:
            node = self._buckets[next_index]
            self._buckets[next_index] = None
            self._size -= 1

            self[node.key] = node.value

            next_index = (next_index + 1) % self._capacity

    def clear(self) -> None:
        self._buckets = [None] * self._capacity
        self._size = 0
