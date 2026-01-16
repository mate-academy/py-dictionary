from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Hashable, Iterator, List


@dataclass
class Node:
    key: Hashable = None
    hash_val: int = None
    value: Any = None


class Dictionary:
    def __init__(
        self,
        initial_capacity: int = 8,
        load_factor: float = 0.75,
        size: int = 0,
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = size
        self.hash_table: List[Node] = [None] * self.capacity

    def __repr__(self) -> str:
        return f"Dictionary{self.hash_table}"

    @property
    def resize_point(self) -> int:
        return int(self.capacity * self.load_factor)

    def _index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __len__(self) -> int:
        """
        Returns the number of key-value pairs in
        the dictionary (i.e., its size)
        """
        return self.size

    def __getitem__(self, key: Hashable) -> Node:
        """
         Retrieves the value associated with a given key.
         Raises a KeyError if the key is not found.
        """
        for node in self.hash_table:
            if node and node.key == key:
                return node.value
        raise KeyError(f"Key not found: {key}")

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """
        Adds or updates a key-value pair in the dictionary.
        Resizes the table if necessary.
        """
        if isinstance(key, (dict, list, set)):
            raise TypeError(
                f"Key must be hashable type! Not {type(key).__name__}!!!"
            )
        if self.size >= self.resize_point:
            self.resize()
        index = self._index(key)
        self.add_to_position(index, key, value)

        while self.hash_table[index]:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity
            self.add_to_position(index, key, value)

    def add_to_position(self, index: int, key: Hashable, value: Any) -> None:
        if not self.hash_table[index]:
            self.hash_table[index] = Node(key, hash(key), value)
            self.size += 1

    def resize(self) -> None:
        """
        Doubles the capacity of the dictionary
        and rehashes all existing key-value pairs.
        """
        self.capacity *= 2
        self.size = 0

        old_table = self.hash_table.copy()
        self.hash_table = [None] * self.capacity

        for node in old_table:
            if node:
                self.__setitem__(node.key, node.value)

    def clear(self) -> None:
        """
        Clears all entries from the dictionary
        and resets it to the initial capacity.
        """
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.size = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        """
        Retrieves the value for the given key, or returns
        a default value if the key is not found.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        """
        Removes and returns the value for the given key.
        If the key is not found, returns the default value.
        """
        index = self._index(key)
        try:
            value = self[key]
            self.hash_table[index] = None
            self.size -= 1
            self.rehash_after_deletion(index)
            return value
        except KeyError:
            return default

    def update(self, other: Dictionary) -> None:
        """
        Updates the dictionary with key-value pairs
        from another dictionary-like object.
        """
        for key, value in other.items:
            self[key] = value

    def __iter__(self) -> Iterator[Hashable]:
        """
        Returns an iterator over the keys in the dictionary.
        """
        for node in self.hash_table:
            if node:
                yield node

    def __delitem__(self, key: Hashable) -> None:
        """
        Removes a key-value pair from the dictionary.
        Rehashes the table after the deletion to maintain performance.
        """
        index = self._index(key)
        while self.hash_table[index]:
            if self.hash_table[index].key == key:
                self.hash_table[index] = None
                self.size -= 1
                self.rehash_after_deletion(index)
                return

    def rehash_after_deletion(self, deleted_index: int) -> None:
        """
        Rehashes entries in the table after a deletion
        to maintain correct lookup behavior.
        """
        index = (deleted_index + 1) % self.capacity
        while self.hash_table[index]:
            node = self.hash_table[index]
            self.hash_table[index] = None
            self.__setitem__(node.key, node.value)
            index = (index + 1) % self.capacity
