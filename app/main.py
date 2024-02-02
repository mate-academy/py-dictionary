from typing import Hashable, Any, List, Optional


DEFAULT_CAPACITY = 8
LOAD_FACTOR_THRESHOLD = 0.7


class Node:
    def __init__(self, key: Hashable, hash_value: int, value: Any) -> None:
        self.key = key
        self.hash_value = hash_value
        self.value = value


class Dictionary:
    def __init__(self) -> None:
        self._capacity: int = DEFAULT_CAPACITY
        self._hash_table: List[Optional[Node]] = [None] * self._capacity
        self._number_of_stored_elements: int = 0

    def __len__(self) -> int:
        return self._number_of_stored_elements

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_of_key: int = hash(key)
        index_to_insert: int = self._find_available_cell(key, hash_of_key)

        if self._hash_table[index_to_insert] is None:
            self._number_of_stored_elements += 1

        self._hash_table[index_to_insert] = Node(key, hash_of_key, value)

        if self._load_factor() > LOAD_FACTOR_THRESHOLD:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index: int = self._find_available_cell(key, hash(key))
        if self._hash_table[index] is None:
            raise KeyError(f"Key {key} not found")

        return self._hash_table[index].value

    def _resize(self) -> None:
        old_table: List[Optional[Node]] = self._hash_table
        self._capacity *= 2
        self._hash_table = [None] * self._capacity
        self._number_of_stored_elements = 0

        for node in old_table:
            if node is not None:
                self.__setitem__(node.key, node.value)

    def _load_factor(self) -> float:
        return self._number_of_stored_elements / self._capacity

    def _find_available_cell(self, key: Hashable, hash_of_key: int) -> int:
        available_cell_index: int = self._get_index_by_hash(hash_of_key)

        while self._is_cell_irrelevant_to_write_key(available_cell_index, key):
            available_cell_index = self._increment_index(available_cell_index)

        return available_cell_index

    def _get_index_by_hash(self, hash_of_key: int) -> int:
        return hash_of_key % self._capacity

    def _increment_index(self, index: int) -> int:
        return (index + 1) % self._capacity

    def _is_cell_irrelevant_to_write_key(
            self,
            available_cell_index: int,
            key: Hashable
    ) -> bool:
        return (
            self._hash_table[available_cell_index] is not None
            and key != self._hash_table[available_cell_index].key
        )
