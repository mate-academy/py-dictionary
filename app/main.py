import copy
from typing import Hashable, Any, Iterable


class Node:
    def __init__(
            self,
            index: int,
            key: Hashable,
            value: Any
    ) -> None:
        self.key = key
        self.index = index
        self.value = value
        self.neighbour = None

    def __repr__(self) -> str:
        return (f"Node with key {self.key}, "
                f"value {self.value} at index {self.index}")


class Dictionary:
    def __init__(self) -> None:
        self._length = 0
        self.hash_table: list[None | Node] = [None] * 8
        self.cur_hash_table: list = []
        self.load_factor = 2 / 3

    def _set(
            self,
            key: Hashable,
            value: Any,
            reset: bool = False
    ) -> None:
        """ Set new key/value pair to dict"""
        hash_key = hash(key)
        key_index = hash_key % len(self.hash_table)
        if self.hash_table[key_index]:
            current_node = self.hash_table[key_index]
            while True:
                # reassign value of key
                if (hash(current_node.key) == hash_key
                        and current_node.key == key):
                    current_node.value = value
                    return
                else:
                    # jump to next node in linked list
                    if current_node.neighbour:
                        current_node = current_node.neighbour
                    # create new neighbour Node at this index
                    else:
                        current_node.neighbour = Node(key_index, key, value)
                        if not reset:
                            self._length += 1
                        return
        else:
            self.hash_table[key_index] = Node(key_index, key, value)
            if not reset:
                self._length += 1
            return

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """Magic method for Dictionary, add new pair to Dictionary
        and controls count of cells in the hash table"""
        self._set(key, value)
        if self._length > self.load_factor * len(self.hash_table):
            self._double_hash_table()

    def _double_hash_table(self) -> None:
        """Increases count of cells in the hash table and set
        new indexes for each key/value pair"""
        self.cur_hash_table = copy.copy(self.hash_table)
        self.hash_table = [None] * len(self.hash_table) * 2
        for elem in self.cur_hash_table:
            if elem:
                self._set(elem.key, elem.value, True)
                if elem.neighbour:
                    current_node = elem.neighbour
                    while True:
                        self._set(current_node.key, current_node.value, True)
                        if current_node.neighbour:
                            current_node = current_node.neighbour
                        else:
                            break
        self.cur_hash_table = []

    def _find_table_index(self, key: Hashable) -> int | Node:
        """Search key in the hash table nodes and returns its index
        in the hash table or parent node"""
        hash_key = hash(key)
        key_index = hash_key % len(self.hash_table)
        if self.hash_table[key_index]:
            current_node = self.hash_table[key_index]
            if (hash(current_node.key) == hash_key
                    and current_node.key == key):
                return key_index
            if current_node.neighbour:
                while True:
                    if (hash(current_node.neighbour.key) == hash_key
                            and current_node.neighbour.key == key):
                        return current_node
                    else:
                        current_node = current_node.neighbour
                        if not current_node.neighbour:
                            raise KeyError(
                                f"This key `{key}` is not present here."
                            )
        else:
            raise KeyError(f"This key `{key}` is not present here.")

    def __getitem__(self, key: Hashable) -> Any:
        """ Returns value of given key"""
        index = self._find_table_index(key)
        if isinstance(index, int):
            return self.hash_table[index].value
        return index.neighbour.value

    def __len__(self) -> int:
        """ Returns count of records in Dictionary"""
        return self._length

    def __repr__(self) -> str:
        """String representation"""
        nodes_list = [
            node.__repr__() for node in self.__iter__(iter_nodes=True)
        ]
        return f"{nodes_list}"

    def __delitem__(self, key: Hashable) -> None:
        """Removes key/value pair from the hash table by given key"""
        index = self._find_table_index(key)
        if isinstance(index, int):
            if self.hash_table[index].neighbour:
                self.hash_table[index] = self.hash_table[index].neighbour
            else:
                self.hash_table[index] = None
        else:
            if index.neighbour.neighbour:
                index.neighbour = index.neighbour.neighbour
            else:
                index.neighbour = None
        self._length -= 1

    def clear(self) -> None:
        """Clear all records in Dictionary"""
        self.hash_table = [None] * 8
        self._length = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        """ Returns value of given key"""
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        """ Deletes key/value pair
        and returns value of given key"""
        try:
            elem = self.__getitem__(key)
            self.__delitem__(key)
            return elem
        except KeyError:
            if default:
                return default
            else:
                raise

    def update(
            self,
            _m: Hashable | Iterable | None = None,
            *args,
            **kwargs
    ) -> None:
        """Reassign value of given key or
        iter through iterable to add or update key/value pairs"""
        if _m:
            if args:
                key, value = _m, args[0]
                self.__setitem__(key, value)
            else:
                iterable = _m
                if isinstance(iterable, dict):
                    for key, value in iterable.items():
                        self.__setitem__(key, value)
                    return
                if hasattr(iterable, "__iter__"):
                    for key, value in iterable:
                        self.__setitem__(key, value)
        else:
            pass

    def __iter__(self, iter_nodes: bool = False) -> Iterable:
        """Iter through keys or nodes in the hash table"""
        for elem in self.hash_table:
            if elem:
                yield elem if iter_nodes else elem.key
                cur_elem = elem.neighbour
                while cur_elem:
                    yield cur_elem if iter_nodes else cur_elem.key
                    cur_elem = cur_elem.neighbour
