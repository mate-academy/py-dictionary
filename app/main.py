from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self._capacity = 8
        self._hash_table = [None] * self._capacity
        self._number_of_stored_elements = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.find_available_index(key)

        if not self._hash_table[index]:

            if (self._number_of_stored_elements
                    >= int(self._capacity * 2 / 3)):
                self._resize()
                index = self.find_available_index(key)

            self._number_of_stored_elements += 1

        self._hash_table[index] = (key, hash(key), value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.find_available_index(key)
        if not self._hash_table[index]:
            raise KeyError(f"{key} is not found")
        return self._hash_table[index][2]

    def __len__(self) -> int:
        return self._number_of_stored_elements

    def find_available_index(self, key: Hashable) -> int:
        index = hash(key) % self._capacity

        while self._hash_table[index] and self._hash_table[index][0] != key:
            index = (index + 1) % self._capacity

        return index

    def _resize(self) -> None:
        self._capacity *= 2
        old_hash_table = self._hash_table
        self._number_of_stored_elements = 0
        self._hash_table = [None] * self._capacity

        for element in old_hash_table:
            if element is not None:
                self[element[0]] = element[2]
