from typing import Any


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value
        self.hash = hash(key)


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def _get_index(self, key_hash: int) -> int:
        return key_hash % self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length / self.capacity >= self.load_factor:
            self._resize()

        node = Node(key, value)
        index = self._get_index(node.hash)

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = node
        self.length += 1

    def __getitem__(self, key: int) -> Any:
        index = self._get_index(hash(key))
        start_index = index

        while self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.capacity
            if index == start_index:
                break

        raise KeyError(
            f"Key Error: The key '{key}' doesn't exist in the dictionary."
        )

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.length = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0
