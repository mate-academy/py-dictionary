from typing import Any

from app.DictionaryIterator import DictionaryIterator


class Node:
    def __init__(self, key: Any, value: Any, key_hash: int) -> None:
        self.key = key
        self.value = value
        self.key_hash = key_hash


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._length = 0
        self._hash_table: list[Node | None] = [None] * self._capacity

    def _hash_index(self, key_hash: int) -> int:
        """get hash index"""
        return key_hash % self._capacity

    def _create_node(
            self,
            index: int,
            key: int,
            value: int,
            key_hash: int
    ) -> None:
        """change size of table and create new node"""
        self._length += 1
        self._hash_table[index] = Node(key, value, key_hash)

    def _check_load_factor(self) -> None:
        """Check load factor and resize it if necessary"""
        if self._length >= int(self._capacity * 2 / 3):
            self._resize()

    def _resize(self) -> None:
        """Resize table, change capacity *= 2 and setitems into new indexes"""
        old_table = self._hash_table
        self._capacity = self._capacity * 2
        self._hash_table = [None] * self._capacity
        self._length = 0
        for node in old_table:
            if node is None:
                continue
            else:
                self.__setitem__(node.key, node.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Add new node, change node, set node to next free position"""
        self._check_load_factor()
        key_hash = hash(key)
        index = self._hash_index(key_hash)

        while True:
            current_node = self._hash_table[index]

            if current_node is None:
                self._create_node(index, key, value, key_hash)
                break

            if current_node.key == key:
                current_node.value = value
                break

            index = (index + 1) % self._capacity

    def __getitem__(self, key: Any) -> Any:
        """get node by key"""
        key_hash = hash(key)
        index = self._hash_index(key_hash)
        initial_index = index

        while True:
            current_node = self._hash_table[index]

            if current_node is None:
                raise KeyError(f"No item with key = {key}")

            if current_node.key == key:
                return current_node.value

            index = (index + 1) % self._capacity
            if index == initial_index:
                raise KeyError(f"No item with key = {key}")

    def __len__(self) -> int:
        """Get length of table"""
        return self._length

    def clear(self) -> None:
        """clear table"""
        self._hash_table = [None] * self._capacity
        self._length = 0

    @staticmethod
    def _can_shift(
            hole_index: int, backward_index: int, ideal_index: int
    ) -> bool:
        if hole_index <= backward_index:
            return (
                ideal_index <= hole_index
                or ideal_index > backward_index
            )
        return hole_index >= ideal_index > backward_index

    def _shift_nodes(self, hole_index: int) -> None:
        """Backward Shift for collision handling after deletion"""
        backward_index = (hole_index + 1) % self._capacity

        while self._hash_table[backward_index] is not None:
            node_to_check = self._hash_table[backward_index]
            ideal_index = self._hash_index(node_to_check.key_hash)

            if self._can_shift(hole_index, backward_index, ideal_index):
                self._hash_table[hole_index] = node_to_check
                self._hash_table[backward_index] = None
                hole_index = backward_index

            backward_index = (backward_index + 1) % self._capacity

    def __delitem__(self, key: Any) -> None:
        """Delete node from table"""
        key_hash = hash(key)
        index = self._hash_index(key_hash)
        initial_index = index

        while True:
            current_node = self._hash_table[index]

            if current_node is None:
                raise KeyError(f"No item with key = {key}")

            if current_node.key == key:
                break

            index = (index + 1) % self._capacity
            if index == initial_index:
                raise KeyError(f"No item with key = {key}")

        self._hash_table[index] = None
        self._length -= 1
        self._shift_nodes(index)

    def get(self, key: Any, value: Any = None) -> Any:
        """get node value by key"""
        key_hash = hash(key)
        index = self._hash_index(key_hash)
        initial_index = index

        while True:
            current_node = self._hash_table[index]

            if current_node is None:
                return value

            if current_node.key == key:
                return current_node.value

            index = (index + 1) % self._capacity
            if index == initial_index:
                return value

    def pop(self, key: Any, default: Any = None) -> Any:
        """pop node by key"""
        key_hash = hash(key)
        index = self._hash_index(key_hash)
        initial_index = index

        while True:
            current_node = self._hash_table[index]

            if current_node is None:
                return default

            if current_node.key == key:
                break

            index = (index + 1) % self._capacity
            if index == initial_index:
                return default

        popped_value = current_node.value
        self._hash_table[index] = None
        self._length -= 1
        self._shift_nodes(index)
        return popped_value

    def update(self, obj: Any) -> None:
        """update nodes"""
        if hasattr(obj, "items"):
            for key, value in obj.items():
                self[key] = value
        else:
            for key, value in obj:
                self[key] = value

    def __iter__(self) -> DictionaryIterator:
        return DictionaryIterator(self._hash_table)
