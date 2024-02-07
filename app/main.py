from typing import Any, Hashable

DEFAULT_CAPACITY = 8


class Dictionary:
    def __init__(self) -> None:
        self._capacity = DEFAULT_CAPACITY
        self._hash_table: list[tuple | None] = [None] * self._capacity
        self._number_of_stored_elements = 0

    def __len__(self) -> int:
        return self._number_of_stored_elements

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_of_key = hash(key)
        index_to_insert = self._find_available_cell(key, hash_of_key)

        if self._hash_table[index_to_insert] is None:
            if self._number_of_stored_elements * 3 >= self._capacity * 2:
                self._resize()
                index_to_insert = self._find_available_cell(key, hash_of_key)
            self._number_of_stored_elements += 1

        self._hash_table[index_to_insert] = (key, hash_of_key, value)

    def __getitem__(self, key: Hashable) -> Any:
        hash_of_key = hash(key)
        index = self._find_available_cell(key, hash_of_key)

        if not self._hash_table[index]:
            raise KeyError(f"Key - {key} does not exist!")

        return self._hash_table[index][2]

    def _resize(self) -> None:
        old_cells = self._hash_table
        self._capacity *= 2
        self._hash_table = [None] * self._capacity
        self._number_of_stored_elements = 0

        for cell in old_cells:
            if cell:
                self[cell[0]] = cell[2]

    def _find_available_cell(self, key: Hashable, hash_of_key: int) -> int:
        available_cell_index = self._get_index_by_hash(hash_of_key)

        while (self._hash_table[available_cell_index] is not None
               and key != self._hash_table[available_cell_index][0]):
            available_cell_index = self._increment_index(available_cell_index)

        return available_cell_index

    def _get_index_by_hash(self, hash_of_key: int) -> int:
        return hash_of_key % self._capacity

    def _increment_index(self, index: int) -> int:
        return (index + 1) % self._capacity
