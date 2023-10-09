from typing import Any, Hashable


class Node:
    def __init__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        self.key = key
        self.hash = hash(key)
        self.value = value


class Dictionary:
    def __init__(
            self,
            initial_capacity: int = 10,
            load_factor: float = 2 / 3
    ) -> None:
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def _resize(
            self
    ) -> None:
        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]
        for chain in self.table:
            if chain:
                for node in chain:
                    index = node.hash % new_capacity
                    new_table[index].append(node)
                    self.table = new_table
                    self.capacity = new_capacity

    def _get_index(
            self,
            key: Hashable
    ) -> int:
        hash_value = hash(key)
        index = hash_value % self.capacity
        return index

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if self.size >= self.capacity * self.load_factor:
            self._resize()
        index_to_insert = self._get_index(key)
        if not self.table[index_to_insert]:
            self.table[index_to_insert] = []
        for node in self.table[index_to_insert]:
            if node.key == key:
                node.value = value
                return
        self.table[index_to_insert].append(Node(key, value))
        self.size += 1

    def __getitem__(
            self,
            key: Hashable
    ) -> Any:
        index_to_search = self._get_index(key)
        if self.table[index_to_search]:
            for node in self.table[index_to_search]:
                if node.key == key:
                    return node.value
        raise KeyError(f"Key {key} not found in the dictionary")

    def __len__(
            self
    ) -> int:
        return self.size

    def __delitem__(
            self,
            key: Hashable
    ) -> None:
        index = hash(key) % self.capacity
        if self.table[index]:
            for index_to_delete, node in enumerate(self.table[index]):
                if node.key == key:
                    del self.table[index][index_to_delete]
                    self.size -= 1
                    return
                raise KeyError(f"Key {key} not found in the dictionary")

    def clear(
            self
    ) -> None:
        self.table = [None] * self.capacity
        self.size = 0

    def update(
            self,
            other_dict: dict
    ) -> None:
        for key, value in other_dict.items():
            self[key] = value

    def __iter__(
            self
    ) -> Any:
        for index in range(self.capacity):
            if self.table[index]:
                for node in self.table[index]:
                    yield node.key
