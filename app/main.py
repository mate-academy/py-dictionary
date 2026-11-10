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
        self.size = 0
        self.table: list[Node | None] = [None] * self.capacity

    def _find_slot(self, key: Hashable, key_hash: int) -> int:
        index = key_hash % self.capacity
        while self.table[index] is not None:
            node = self.table[index]
            if node.hash == key_hash and node.key == key:
                return index
            index = (index + 1) % self.capacity
        return index

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        for node in old_table:
            if node is not None:
                index = self._find_slot(node.key, node.hash)
                self.table[index] = node

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = self._find_slot(key, key_hash)

        if self.table[index] is not None:
            self.table[index].value = value
            return

        if self.size + 1 > self.capacity * self.load_factor:
            self._resize()
            index = self._find_slot(key, key_hash)

        self.table[index] = Node(key, key_hash, value)
        self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_slot(key, hash(key))
        if self.table[index] is None:
            raise KeyError(key)
        return self.table[index].value

    def __len__(self) -> int:
        return self.size
