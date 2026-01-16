from typing import Any, Optional, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length: int = 0
        self.capacity: int = 8
        self.hash_table: list[Optional[tuple]] = [None] * self.capacity

    def _get_key_value(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        original_index = index

        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity

            if index == original_index:
                break

        return None

    def _set_key_value(self, key: Hashable, value: Any) -> None:
        self._check_extend_memory()

        index = hash(key) % self.capacity
        original_index = index

        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, hash(key), value)
                return
            index = (index + 1) % self.capacity

            if index == original_index:
                break

        self.hash_table[index] = (key, hash(key), value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        value = self._get_key_value(key)
        if value is None:
            raise KeyError
        return value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._set_key_value(key, value)

    def __len__(self) -> int:
        return self.length

    def _re_sort_memory(self, old_table: list) -> None:
        for entry in old_table:
            if entry is not None:
                # it == self.__setitem__(entry[0], entry[2])
                self[entry[0]] = entry[2]

    def _check_extend_memory(self) -> None:
        if self.length >= (2 / 3) * self.capacity:
            old_table = self.hash_table
            self.capacity *= 2
            self.hash_table = [None] * self.capacity
            self.length = 0

            self._re_sort_memory(old_table)
