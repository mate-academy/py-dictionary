DEFAULT_CAPACITY = 8


class Dictionary:
    def __init__(self) -> None:
        self._capacity: int = DEFAULT_CAPACITY
        self._hash_table: list = [None] * self._capacity
        self._number_of_stored_elements: int = 0

    def __len__(self) -> int:
        return self._number_of_stored_elements

    def __setitem__(self, key: any, value: any) -> None:
        if self._number_of_stored_elements > self._capacity * 0.7:
            self._resize()

        hash_of_key: int = hash(key)
        index_to_insert: int = self._find_available_cell(key, hash_of_key)

        if self._hash_table[index_to_insert] is None:
            self._number_of_stored_elements += 1

        self._hash_table[index_to_insert] = (key, hash_of_key, value)

    def _find_available_cell(self, key: any, hash_of_key: int) -> int:
        available_cell_index = self._get_index_by_hash(hash_of_key)

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
            key: any
    ) -> bool:
        return (
            self._hash_table[available_cell_index] is not None
            and key != self._hash_table[available_cell_index][0]
        )

    def __getitem__(self, key: any) -> any:
        hash_of_key = hash(key)
        index = self._find_available_cell(key, hash_of_key)
        if self._hash_table[index] is None:
            raise KeyError(f"Key {key} not found")
        return self._hash_table[index][2]

    def _resize(self) -> None:
        self._capacity *= 2
        old_hash_table = self._hash_table
        self._hash_table = [None] * self._capacity
        self._number_of_stored_elements = 0
        for item in old_hash_table:
            if item is not None:
                self[item[0]] = item[2]
