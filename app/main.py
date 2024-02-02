from typing import Hashable, Any
DEFAULT_CAPACITY = 8


class Dictionary:

    def __init__(self) -> None:
        self._capacity = DEFAULT_CAPACITY
        self._hash_table: list = [None] * self._capacity
        self._stored_element = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._find_available_call(key)

        if self._hash_table[index] is None:
            self._stored_element += 1
        self._hash_table[index] = (key, hash(key), value)
        if self._stored_element * 3 >= self._capacity * 2:
            self._capacity *= 2
            self._stored_element = 0
            self._resize_hash_table()

    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_available_call(key)
        if self._hash_table[index] is None:
            raise KeyError(f"{key}")
        return self._hash_table[index][2]

    def _resize_hash_table(self) -> None:
        last_hash_table = self._hash_table
        self._hash_table = [None] * self._capacity
        for node in last_hash_table:
            if node:
                self.__setitem__(node[0], node[2])

    def _get_index(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def _find_available_call(self, key: Hashable) -> int:
        available_index = self._get_index(key)
        while (
                self._hash_table[available_index] is not None
                and key != self._hash_table[available_index][0]
        ):
            available_index += 1
            available_index %= self._capacity
        return available_index

    def clear(self) -> None:
        self._hash_table = [None] * DEFAULT_CAPACITY

    def get(self, keyname: Hashable, value: Any = None) -> Any:
        index = self._find_available_call(keyname)
        if self._hash_table[index]:
            value = self._hash_table[index][2]
        return value

    def pop(self, keyname: Hashable) -> Any:
        index = self._find_available_call(keyname)
        value = self._hash_table[index][2]
        self.__delitem__(key=keyname)
        return value

    def __delitem__(self, key: Hashable) -> None:
        index = self._find_available_call(key)
        self._hash_table[index] = None
        self._stored_element -= 1
        if self._stored_element * 3 < self._capacity * 2:
            self._capacity //= 2
            self._stored_element = 0
            self._resize_hash_table()

    def __len__(self) -> int:
        return self._stored_element

    def __iter__(self) -> iter:
        return iter(key[0] for key in self._hash_table if key)
