from typing import Hashable, Any


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self._size = 0
        self._capacity = 8
        self._threshold = int(self._capacity * Dictionary.LOAD_FACTOR)
        self._hash_table = [[] for _ in range(self._capacity)]

    def resize(self) -> None:
        new_hash_table = self._hash_table.copy()
        self._capacity *= 2
        self._size = 0
        self._threshold = int(self._capacity * Dictionary.LOAD_FACTOR)
        self._hash_table = [[] for _ in range(self._capacity)]

        for element in new_hash_table:
            if element:
                self.__setitem__(element[0], element[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._size == self._threshold:
            self.resize()

        hash_value = hash(key)
        hash_index = hash_value % self._capacity

        while True:
            if not self._hash_table[hash_index]:
                self._hash_table[hash_index] = [key, hash_value, value]
                self._size += 1
                break

            if self._hash_table[hash_index][0] == key \
                    and self._hash_table[hash_index][1] == hash_value:
                self._hash_table[hash_index][2] = value
                break

            hash_index = (hash_index + 1) % self._capacity

    def __getitem__(self, key: Hashable) -> Any | KeyError:
        hash_value = hash(key)
        hash_index = hash_value % self._capacity

        while self._hash_table[hash_index]:
            if self._hash_table[hash_index][0] == key \
                    and self._hash_table[hash_index][1] == hash_value:
                return self._hash_table[hash_index][2]

            hash_index = (hash_index + 1) % self._capacity

        raise KeyError

    def __len__(self) -> int:
        return self._size
