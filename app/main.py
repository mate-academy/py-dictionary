from __future__ import annotations
from typing import Hashable, Any, Iterable


class Dictionary:
    def __init__(self, *args, **kwargs) -> None:
        self._capacity = 8
        self._length = 0
        self._load_factor = 2 / 3
        self._threshold = int(self._capacity * self._load_factor)
        self._hash_table = [[]] * self._capacity
        self._is_iterator = False
        self._default_value = None

        if args:
            for arg in args:
                self[arg] = self._default_value

        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._is_iterator:
            raise TypeError("'my_special_dict_keyiterator' object"
                            "doen't support item assignment")

        key_hash = hash(key)
        node = [key, key_hash, value]
        index = key_hash % self._capacity

        while True:
            if not self._hash_table[index]:
                self._hash_table[index] = node
                self._length += 1
                break
            if self._hash_table[index][:2] == node[:2]:
                self._hash_table[index][2] = value
                break
            index = (index + 1) % self._capacity

        if self._length > self._threshold:
            self._resize_array()

    def __getitem__(self, key: Hashable) -> Any:
        if self._is_iterator:
            raise TypeError("'my_special_dict_keyiterator' object "
                            "is not subscriptable")

        key_hash = hash(key)
        index = key_hash % self._capacity

        while self._hash_table[index]:
            if self._hash_table[index][:2] == [key, key_hash]:
                return self._hash_table[index][2]
            index = (index + 1) % self._capacity

        raise KeyError

    def __delitem__(self, key: Hashable) -> None:
        if self._is_iterator:
            raise TypeError("'my_special_dict_keyiterator' object doesn't "
                            "support item deletion")

        index = hash(key) % self._capacity

        while True:
            node = self._hash_table[index]
            if not node:
                raise KeyError
            if node[0] == key:
                self._length -= 1
                self._hash_table[index] = []
                self._move_nodes(index)
                break
            else:
                index = (index + 1) % self._capacity

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Dictionary:
        self._is_iterator = True
        self.current_index = 0
        return self

    def __next__(self) -> Any:
        while True:
            if self.current_index >= self._capacity:
                raise StopIteration

            node = self._hash_table[self.current_index]
            self.current_index += 1
            if node:
                return node[0]

    def __contains__(self, item: Hashable) -> bool:
        return True if item in self.keys() else False

    def __eq__(self, other: Dictionary) -> bool:
        if self._length != other._length:
            return False

        for index in range(len(self)):
            if self[index] != other[index]:
                return False

        return True

    def __str__(self) -> str:
        data = [f"{node[0]}: {node[2]}" for node in self._hash_table if node]
        return f"< {', '.join(data)} >"

    def __add__(self, other: Dictionary) -> Dictionary:
        if isinstance(other, Dictionary):
            new_dictionary = Dictionary()
            for key, value in self.items().items():
                new_dictionary[key] = value
            for key, value in other.items().items():
                new_dictionary[key] = value

            return new_dictionary

        raise TypeError("can only concatenate Dictionary to Dictionary")

    def _resize_array(self) -> None:
        self._capacity *= 2
        self._length = 0
        self._threshold = int(self._capacity * self._load_factor)

        old_table = self._hash_table
        self._hash_table = [[]] * self._capacity

        for node in old_table:
            if node:
                self[node[0]] = node[2]

    def _move_nodes(self, index: int) -> None:
        last_index = index

        while True:
            index = (index + 1) % self._capacity
            node = self._hash_table[index]
            if not node:
                break
            real_index_node = hash(node[0]) % self._capacity
            if index != real_index_node:
                self._hash_table[last_index] = node
                self._hash_table[index] = []
                last_index = index

    def update(self, iter_obj: Iterable) -> None:
        if isinstance(iter_obj, (tuple, list, str)):
            for key in iter_obj:
                self[key] = self._default_value
            return
        if isinstance(iter_obj, dict):
            for key, value in iter_obj.items():
                self[key] = value
            return
        if isinstance(iter_obj, Dictionary):
            for key, value in iter_obj.items().items():
                self[key] = value
                return

        raise TypeError(f"{type(iter_obj)} is not iterable")

    def clear(self) -> None:
        self._length = 0
        self._hash_table = [[]] * self._capacity

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Hashable) -> Any:
        value = self[key]
        del self[key]

        return value

    def keys(self) -> list:
        return [node[0] for node in self._hash_table if node]

    def values(self) -> list:
        return [node[2] for node in self._hash_table if node]

    def items(self) -> dict:
        return {node[0]: node[2] for node in self._hash_table if node}

    def count_values(self, item: Any) -> int:
        return self.values().count(item)

    def set_default_value(self, value: Any) -> None:
        self._default_value = value
