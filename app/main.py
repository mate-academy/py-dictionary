from typing import Any, Hashable

DEFAULT_CAPACITY = 8


class Dictionary:

    def __init__(self) -> None:
        self._capacity = DEFAULT_CAPACITY
        self._hash_table = [None] * self._capacity
        self._length = 0

    def __len__(self) -> int:
        return self._length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index_insert = self._find_available_cell(key, key_hash)
        threshold = int(self._capacity * 2 / 3)

        if self._hash_table[index_insert] is None:

            if self._length + 1 >= threshold:
                self._resize()

            self._length += 1

        self._hash_table[index_insert] = (key, key_hash, value)

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = self._get_index_by_hash(key_hash)

        for _ in range(self._capacity):
            if (self._hash_table[index] is not None
                    and key == self._hash_table[index][0]):
                return self._hash_table[index][2]

            index = self._increment_index(index)

        raise KeyError(f"{key} not exist!")

    def _resize(self) -> None:

        old_hash_table = self._hash_table.copy()
        self._capacity *= 2
        self._hash_table = [None] * self._capacity
        self._length = 0

        for cell in old_hash_table:
            if cell is not None:
                self[cell[0]] = cell[2]

    def _find_available_cell(self, key: Hashable, key_hash: int) -> int:
        available_cell_index = self._get_index_by_hash(key_hash)

        while True:
            cell = self._hash_table[available_cell_index]
            if cell is None:
                return available_cell_index
            if cell[0] == key:
                return available_cell_index
            available_cell_index = self._increment_index(available_cell_index)

    def _get_index_by_hash(self, key_hash: int) -> int:
        return key_hash % self._capacity

    def _increment_index(self, index: int) -> int:
        return (index + 1) % self._capacity

    def _is_cell_irrelevant_to_write_key(self,
                                         index: int,
                                         key: Hashable) -> bool:
        return (
            self._hash_table[index] is not None
            and key != self._hash_table[index][0]
        )
