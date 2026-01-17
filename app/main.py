from typing import Hashable, Any

DEFAULT_CAPACITY = 8


class Dictionary:
    def __init__(self) -> None:
        self._capacity = DEFAULT_CAPACITY
        self._number_of_elements = 0
        self._hash_table: list = [None] * self._capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_of_key = hash(key)
        index_to_insert = self._get_index(key, hash_of_key)

        if self._hash_table[index_to_insert] is None:
            self._number_of_elements += 1

            if self._number_of_elements * 3 >= self._capacity * 2:
                self._resize()
                self[key] = value
                return

        self._hash_table[index_to_insert] = (key, hash_of_key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self._get_index(key, hash(key))
        if self._hash_table[index]:
            return self._hash_table[index][2]
        raise KeyError(f"{key} is not found")

    def __len__(self) -> int:
        return self._number_of_elements

    def _get_index(self, key: Hashable, hash_of_key: int) -> int:
        available_cell_index = self._get_index_by_hash(hash_of_key)

        while (
                self._hash_table[available_cell_index] is not None
                and key != self._hash_table[available_cell_index][0]
        ):
            available_cell_index += 1
            available_cell_index %= self._capacity

        return available_cell_index

    def _get_index_by_hash(self, hash_of_key: int) -> int:
        return hash_of_key % self._capacity

    def _resize(self) -> None:
        self._capacity *= 2
        old_hash_table = self._hash_table
        self._hash_table: list = [None] * self._capacity
        self._number_of_elements = 0

        for item in old_hash_table:
            if item is not None:
                self[item[0]] = item[2]
