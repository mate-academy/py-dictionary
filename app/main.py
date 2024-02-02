from typing import Hashable


class Dictionary:
    def __init__(self) -> None:
        self._length_of_dict = 0
        self._capacity = 8
        self._hash_table = [None] * self._capacity

    def __len__(self) -> int:
        return self._length_of_dict

    def __setitem__(self, key: Hashable, value: any) -> None:
        key_hash = hash(key)
        index_in_hash_table = self._find_available_cell(key, key_hash)
        if self._hash_table[index_in_hash_table] is None:
            self._length_of_dict += 1
            if self._length_of_dict >= int(self._capacity * 2 / 3):
                self._resize_hash_table()
                self[key] = value
                return

        self._hash_table[index_in_hash_table] = (key, key_hash, value)

    def __getitem__(self, key: Hashable) -> any:
        index_get = self._find_available_cell(key, hash(key))
        if self._hash_table[index_get] is None:
            raise KeyError
        return self._hash_table[index_get][2]

    def _resize_hash_table(self) -> None:
        self._capacity *= 2
        old_hash_table = self._hash_table
        self._hash_table = [None] * self._capacity
        self._length_of_dict = 0
        for element in old_hash_table:
            if element is not None:
                self[element[0]] = element[2]

    def _index_is_available(self, key: Hashable, index: int) -> bool:
        return (self._hash_table[index] is not None
                and key != self._hash_table[index][0])

    def _find_available_cell(self, key: Hashable, hash_key: int) -> int:
        element_index = hash_key % self._capacity
        while self._index_is_available(key, element_index):
            element_index += 1
            element_index %= self._capacity
        return element_index
