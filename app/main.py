from dataclasses import dataclass
from typing import Any, Hashable


@dataclass
class Node:
    key: Hashable
    value: Any
    key_hash: int

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}"


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self._capacity = capacity
        self._length = 0
        self._load_factor = self._capacity * 2 // 3
        self._hash_table: list[Node | None] = [None] * self._capacity

    def __len__(self) -> int:
        return self._length

    def __repr__(self) -> str:
        return ", ".join([f"({node})" for node in self._hash_table])

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self._capacity

        while self._hash_table[index]:
            if self._hash_table[index].key_hash == key_hash:
                if self._hash_table[index].key == key:
                    return self._hash_table[index].value
            index = (index + 1) % self._capacity

        if not self._hash_table[index]:
            raise KeyError(f"Key `{key}` is not in this dictionary.")

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self._capacity

        while self._hash_table[index]:
            if self._hash_table[index].key_hash == key_hash:
                if self._hash_table[index].key == key:
                    self._hash_table[index].value = value
                    return
            index = (index + 1) % self._capacity

        if self._length == self._load_factor:
            self._resize()
            return self.__setitem__(key, value)

        self._hash_table[index] = Node(key, value, key_hash)
        self._length += 1

    def _resize(self) -> None:
        previous_nodes = [node for node in self._hash_table if node]
        self.__init__(self._capacity * 2)

        for node in previous_nodes:
            self.__setitem__(node.key, node.value)

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = key_hash % self._capacity
        end_index = (index + self._capacity - 1) % self._capacity

        while index != end_index:
            if self._hash_table[index]:
                if self._hash_table[index].key_hash == key_hash:
                    if self._hash_table[index].key == key:
                        self._hash_table[index] = None
                        self._length -= 1
                        return
            index = (index + 1) % self._capacity

        raise KeyError(f"Key `{key}` is not in this dictionary.")

    def clear(self) -> None:
        self.__init__()
