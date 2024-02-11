from typing import Hashable, Any


class Node:

    def __init__(self, key: Hashable, value: Any) -> None:
        self.key = key
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.number_of_items = 0

    def __len__(self) -> int:
        return self.number_of_items

    def _get_index_by_key(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            index = index + 1
            if index > self.capacity - 1:
                index = 0
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        for bucket in self.hash_table:
            if bucket is not None:
                if bucket[0].key == key:
                    bucket[0].value = value
                    return
        index = self._get_index_by_key(key)
        self.hash_table[index] = []
        self.hash_table[index].append(Node(key, value))
        self.number_of_items += 1
        if self.number_of_items > self.capacity * (2 / 3):
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        for bucket in self.hash_table:
            if bucket is not None:
                if bucket[0].key == key:
                    return bucket[0].value
        raise KeyError(f"Key '{key}' not found")

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.number_of_items = 0
        for bucket in old_table:
            if bucket is not None:
                for node in bucket:
                    self.__setitem__(node.key, node.value)
