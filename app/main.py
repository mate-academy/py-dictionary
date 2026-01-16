from typing import Any, Hashable, Iterator
from dataclasses import dataclass


class Dictionary:
    """A class to create a dictionary."""

    def __init__(self) -> None:
        """Constructs all the necessary attributes for Dictionary object."""
        self.number_of_elements = 0
        self.initial_capacity = 8
        self.hash_table = [[] for _ in range(self.initial_capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """
        Create key-value pair in dictionary with [] indexer operator.
        Check for collision and key exist in dictionary.
        Run value reassign and resize dictionary if necessary.
        """
        index = self.get_hash_value_and_index(key)
        node = self.create_node((key, value))
        if self.no_collision(self.hash_table, index):
            self.hash_table[index].append(node)
            self.number_of_elements += 1
        elif not self.key_exists(self.hash_table[index], key):
            self.hash_table[index].append(node)
            self.number_of_elements += 1
        else:
            self.value_reassign(index, key, value)
        if self.load_factor():
            self.resize_hash_table()

    def __getitem__(self, key: Hashable) -> Any:
        """Return value with use of [] indexer operator"""
        index = self.get_hash_value_and_index(key)
        bucket = self.hash_table[index]
        for node in bucket:
            if node.key == key:
                return node.value
        raise KeyError("Key does not exist")

    def __delitem__(self, key: Hashable) -> None:
        """Remove an item from the dictionary by its key."""
        index = self.get_hash_value_and_index(key)
        bucket = self.hash_table[index]
        for node in bucket:
            if node.key == key:
                bucket.remove(node)
                self.number_of_elements -= 1
                return
        raise KeyError(key)

    def __iter__(self) -> Iterator[list[Any]]:
        """Return an iterator over the keys of the dictionary."""
        return iter(self.hash_table)

    def __len__(self) -> int:
        """Return the number of key-value pairs in dictionary."""
        return self.number_of_elements

    def clear(self) -> None:
        """Remove all the elements from the dictionary"""
        self.hash_table = [[] for _ in range(self.initial_capacity)]

    def get(self, key: Hashable, value: Any = None) -> None:
        """Return the value of the specified key."""
        try:
            return self.__getitem__(key)
        except KeyError:
            return value

    def pop(self, key: Hashable) -> None:
        """Remove the element with the specified key."""
        return self.__delitem__(key)

    def update(self, key: Hashable, value: Any) -> None:
        """Update the dictionary with the specified key-value pairs."""
        self.__setitem__(key, value)

    @dataclass
    class Node:
        """
        A class to create a node in dictionary.
        Node contains hash value, key and value.
        """
        hash_value: int
        key: Hashable
        value: Any

    @staticmethod
    def hash_value(key: Hashable) -> int:
        """Return hash value."""
        return hash(key)

    def get_node_index(self, hash_value: Any) -> int:
        """Return node index."""
        return hash_value % self.initial_capacity

    def get_hash_value_and_index(self, key: Hashable) -> int:
        """
        Unite hash_value and get_node_index
        functions and returns node index.
         """
        hash_value = self.hash_value(key)
        index = self.get_node_index(hash_value)
        return index

    @staticmethod
    def create_node(items: tuple) -> Node:
        """Create Node instance"""
        hash_value = hash(items[0])
        key = items[0]
        value = items[1]
        return Dictionary.Node(hash_value, key, value)

    @staticmethod
    def no_collision(hash_table: list, index: int) -> bool:
        """
        Check if collision does not exist.
        Length of empty dictionary cell (bucket) should be 0.
        """
        return len(hash_table[index]) == 0

    @staticmethod
    def key_exists(bucket: list[Node], key: Hashable) -> bool:
        """Check if key already exists"""
        for node in bucket:
            if node.key == key:
                return True
        return False

    def value_reassign(self, index: int, key: Hashable, value: Any) -> None:
        """Reassign key value"""
        bucket = self.hash_table[index]
        for node in bucket:
            if node.key == key:
                node.value = value

    def load_factor(self) -> bool:
        """Check if the number of elements > 2/3 * table size"""
        limit_load = 0.67 * self.initial_capacity
        return self.number_of_elements > limit_load

    def resize_hash_table(self) -> None:
        """Resize hash table and enumerate values"""
        self.initial_capacity *= 2
        temporary_hash_table = [[] for _ in range(self.initial_capacity)]
        for bucket in self.hash_table:
            if len(bucket) != 0:
                for node in bucket:
                    new_index = self.get_node_index(node.hash_value)
                    temporary_hash_table[new_index].append(node)
        self.hash_table = temporary_hash_table
        del temporary_hash_table
