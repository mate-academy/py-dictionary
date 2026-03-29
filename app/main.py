from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._hash_table: list = [None] * self._capacity
        self._number_of_stored_elements = 0

    def _get_hash(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        self._capacity *= 2
        self._number_of_stored_elements = 0
        copy_of_old_table = self._hash_table
        self._hash_table = [None] * self._capacity

        for node in copy_of_old_table:
            if node is not None:
                self[node[0]] = node[2]

    def _find_available_cell(self, key: Hashable) -> int:
        index = self._get_hash(key)
        while (
            self._hash_table[index] is not None
            and self._hash_table[index][0] != key
        ):
            index += 1
            index %= self._capacity
        return index

    def __len__(self) -> int:
        return self._number_of_stored_elements

    def __getitem__(self, item: int) -> Any:
        index = self._find_available_cell(item)
        if self._hash_table[index] is None:
            raise KeyError
        return self._hash_table[index][2]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_ = self._get_hash(key)
        index_to_insert = self._find_available_cell(key)

        if self._hash_table[index_to_insert] is None:
            self._number_of_stored_elements += 1
            if self._number_of_stored_elements >= self._capacity / 3 * 2:
                self._resize()
                self[key] = value
                return

        self._hash_table[index_to_insert] = (key, hash_, value)
