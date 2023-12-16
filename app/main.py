from typing import Any, Hashable


class Node:
    def __init__(self, key: Hashable, value: Any, _hash: int) -> None:
        self.key = key
        self.value = value
        self.hash = _hash


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.node_qty = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.node_qty > self.capacity * self.load_factor:
            self._resize()
        hash_index = self._get_index(key)
        while (
                self.table[hash_index]
                and self.table[hash_index].key != key
        ):
            hash_index += 1
            hash_index %= self.capacity

        if self.table[hash_index] is None:
            self.table[hash_index] = Node(key, value, hash(key))
            self.node_qty += 1

        else:
            self.table[hash_index].value = value

    def __getitem__(self, key: Hashable) -> Any:
        hash_index = self._get_index(key)
        while (
                self.table[hash_index]
                and self.table[hash_index].key != key
        ):
            hash_index += 1
            hash_index %= self.capacity

        if self.table[hash_index] is None:
            raise KeyError

        return self.table[hash_index].value

    def __len__(self) -> int:
        return self.node_qty

    def _get_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        self.capacity *= 2
        old_bucket = self.table
        self.table = self.capacity * [None]
        self.node_qty = 0

        for node in old_bucket:
            if node:
                self[node.key] = node.value

    def clear(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.node_qty = 0
        self.table = [None] * self.capacity

    def __delitem__(self, key: Hashable) -> None:
        hash_index = self._get_index(key)
        if self.table[hash_index]:
            self.table[hash_index] = None
            self.node_qty -= 1
        raise KeyError(key)

    def get(self, key: Hashable) -> Any:
        return self[key] if key in self else None

    def update(self, new_dict: dict) -> None:
        for key, value in new_dict.items():
            self.__setitem__(key, value)
