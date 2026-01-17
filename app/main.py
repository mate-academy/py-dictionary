from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * 8
        self.load_factor = 2 / 3
        self.size = 0

    def __repr__(self) -> str:
        return str(
            {
                item[0]: item[2]
                for item in self.hash_table
                if item is not None
            }
        )

    def _get_node_index(self, key: Hashable, capacity: int) -> int:
        """ Computes node index based on the key hash """
        node_index = hash(key) % capacity
        while (self.hash_table[node_index]
               and self.hash_table[node_index][0] != key):
            node_index = (node_index + 1) % self.capacity
        return node_index

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_hash_table = [None] * new_capacity
        for node in self.hash_table:
            if node:
                key, *_ = node
                new_node_index = hash(key) % new_capacity
                while new_hash_table[new_node_index]:
                    new_node_index = (new_node_index + 1) % new_capacity
                new_hash_table[new_node_index] = (key, *_)
        self.hash_table = new_hash_table
        self.capacity = new_capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """ Stores a new key-value pair or updates existing. """
        node_index = self._get_node_index(key, self.capacity)
        node = (key, hash(key), value)
        if (self.hash_table[node_index]
                and self.hash_table[node_index][0] == key):
            self.hash_table[node_index] = node
        else:
            self.hash_table[node_index] = node
            self.size += 1
        if self.size / self.capacity >= self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> str | int:
        """ Looks up a value with the specified key """
        node_index = self._get_node_index(key, self.capacity)
        if self.hash_table[node_index]:
            return self.hash_table[node_index][2]
        raise KeyError(f"Key {key} doesn't exist.")

    def __delitem__(self, key: Hashable) -> None:
        """ Deletes item with the specified key """
        node_index = self._get_node_index(key, self.capacity)
        if self.hash_table[node_index]:
            self.hash_table[node_index] = None
            self.size -= 1

    def __len__(self) -> int:
        return self.size

    def get(self, key: Hashable, default: Any = None) -> Any:
        """ Returns a value of the specified key, otherwise default value """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        """ Removes the element with the specified key """
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            return default

    def update(self, other_dict: dict) -> None:
        """ Updates the dictionary with the specified key-value pairs """
        for key, value in other_dict.items():
            self[key] = value

    def __iter__(self) -> None:
        for node in self.hash_table:
            if node:
                yield node[0]

    def clear(self) -> None:
        """ Removes all the elements from the dictionary """
        self.hash_table = [None] * self.capacity
        self.size = 0
