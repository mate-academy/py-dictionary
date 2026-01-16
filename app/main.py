from typing import Hashable, Any


class Dictionary:

    class Node:

        def __init__(self, key: Hashable, value: Any, hash_key: int) -> None:
            self.key = key
            self.value = value
            self.hash_key = hash_key

    DEFAULT_CAPACITY = 8

    def __init__(self) -> None:
        self.capacity = Dictionary.DEFAULT_CAPACITY
        self.hash_table: list[tuple | None] = [None] * self.capacity
        self.number_of_elements = 0

    def __len__(self) -> int:
        return self.number_of_elements

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.number_of_elements >= self.capacity * 0.75:
            self.resize()

        hash_key = hash(key)
        index_to_past = self.find_or_insert_index(key, hash_key)

        if self.hash_table[index_to_past] is None:
            self.number_of_elements += 1

        self.hash_table[index_to_past] = Dictionary.Node(key, value, hash_key)

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index_to_search = self.find_or_insert_index(key, hash_key)

        if self.hash_table[index_to_search] is not None:
            return self.hash_table[index_to_search].value
        else:
            raise KeyError(f"Key {key} not found")

    def resize(self) -> None:
        old_cases = self.hash_table
        self.capacity *= 2
        self.hash_table: list[tuple | None] = [None] * self.capacity
        self.number_of_elements = 0

        for node in old_cases:
            if node:
                self[node.key] = node.value

    def find_or_insert_index(self, key: Hashable, hash_key: int) -> int:
        index = self.get_index_by_hash(hash_key)
        while self.hash_table[index] is not None and (
            self.hash_table[index].key != key
            or self.hash_table[index].hash_key != hash_key
        ):
            index = self.increment_index(index)
        return index

    def get_index_by_hash(self, hash_key: int) -> int:
        return hash_key % self.capacity

    def increment_index(self, index: int) -> int:
        return (index + 1) % self.capacity
