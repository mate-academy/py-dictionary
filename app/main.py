from typing import Any, Hashable


class Node:
    def __init__(
        self,
        key: Hashable,
        hash_value: int,
        value: Any
    ) -> None:
        self.key = key
        self.hash = hash_value
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.length = 0
        self.hash_table: list[Node | None] = [None] * self.capacity

    def _find_slot(self, key: Hashable, key_hash: int) -> int:
        index = key_hash % self.capacity
        while self.hash_table[index] is not None:
            node = self.hash_table[index]
            if node.hash == key_hash and node.key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for node in old_table:
            if node is not None:
                index = self._find_slot(node.key, node.hash)
                self.hash_table[index] = node

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)

        if self.hash_table[index] is not None:
            self.hash_table[index].value = value
            return

        if self.length + 1 > self.capacity * self.load_factor:
            self._resize()
            index = self._find_slot(key, key_hash)

        self.hash_table[index] = Node(key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_slot(key, hash(key))
        if self.hash_table[index] is None:
            raise KeyError(key)
        return self.hash_table[index].value

    def __len__(self) -> int:
        return self.length
