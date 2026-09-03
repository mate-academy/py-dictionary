from typing import Any


class Node:
    def __init__(
            self,
            key: Any,
            key_hash: int,
            value: Any) -> None:
        self.key = key
        self.hash = key_hash
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table = [None] * self.capacity

    def _index_for_key(
            self,
            key: Any,
            key_hash: int
    ) -> int:
        idx = key_hash % self.capacity
        while self.hash_table[idx] is not None:
            node = self.hash_table[idx]
            if node.hash == key_hash and node.key == key:
                return idx
            idx = (idx + 1) % self.capacity
        return idx

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0
        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= self.capacity * 2 / 3:
            self._resize()

        key_hash = hash(key)
        idx = self._index_for_key(key, key_hash)

        if self.hash_table[idx] is None:
            self.hash_table[idx] = Node(key, key_hash, value)
            self.length += 1
        else:
            self.hash_table[idx].value = value

    def __getitem__(self, key: Any) -> Any:
        key_hash = hash(key)
        idx = self._index_for_key(key, key_hash)
        if self.hash_table[idx] is None:
            raise KeyError(key)
        return self.hash_table[idx].value

    def __len__(self) -> int:
        return self.length
