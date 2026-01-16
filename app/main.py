import dataclasses
from typing import Any, Optional


class Dictionary:
    def __init__(self) -> None:
        self._length: int = 0
        self._hash_table: list[Optional["DictNode"]] = [None] * 8
        self._trash_holder: int = 5

    def __setitem__(self, key: Any, value: Any) -> None:
        node: DictNode = Dictionary._make_node(key, value)
        index: int = self._collision_handler(node)

        if not self._hash_table[index]:
            self._length += 1

        self._hash_table[index] = node

        if self._length > self._trash_holder:
            self._resize_table()

    def __getitem__(self, key: Any) -> Any:
        index: int = self._make_index(hash(key))
        node: Optional[DictNode] = self._hash_table[index]

        if node and node.key == key:
            return node.value
        return self._node_finder(key)

    def __len__(self) -> int:
        return self._length

    def _make_index(self, hash_value: int) -> int:
        return hash_value % len(self._hash_table)

    @staticmethod
    def _make_node(key: Any, value: Any) -> "DictNode":
        return DictNode(
            key=key,
            dict_hash=hash(key),
            value=value
        )

    def _resize_table(self) -> None:
        old_table: list[Optional[DictNode]] = self._hash_table
        new_size: int = len(self._hash_table) * 2
        self._hash_table = [None] * new_size
        self._trash_holder = int(new_size * (2 / 3))

        for node in old_table:
            if node:
                index: int = self._make_index(node.dict_hash)
                while self._hash_table[index] is not None:
                    index = (index + 1) % len(self._hash_table)
                self._hash_table[index] = node

    def _node_finder(self, key: Any) -> Any:
        index: int = self._make_index(hash(key))
        start: int = index

        while True:
            node: Optional[DictNode] = self._hash_table[index]
            if node and node.key == key:
                return node.value

            index = (index + 1) % len(self._hash_table)
            if index == start:
                break

        raise KeyError("Key not found")

    def _collision_handler(self, node: "DictNode") -> int:
        index: int = self._make_index(node.dict_hash)

        while self._hash_table[index] is not None:
            if node.key == self._hash_table[index].key:
                return index
            index = (index + 1) % len(self._hash_table)

        return index


@dataclasses.dataclass
class DictNode:
    key: Any
    dict_hash: int
    value: Any
