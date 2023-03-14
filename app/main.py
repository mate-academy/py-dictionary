from typing import Any, Hashable


class Dictionary:

    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table: list = [None] * self.capacity

    def resize(self) -> None:
        hash_table_to_resize = self.hash_table
        self.capacity *= 2
        self.hash_table: list = [None] * self.capacity
        self.length = 0
        for node in hash_table_to_resize:
            if node:
                key, value, hash_value = node
                self.__setitem__(key, value)

    def find_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
            self.hash_table[index]
            and self.hash_table[index][0] != key
        ):
            index = (index + 1) % self.capacity

        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.find_index(key)

        if not self.hash_table[index]:
            if self.length > int(self.capacity * self.LOAD_FACTOR):
                self.resize()
                return self.__setitem__(key, value)

            self.length += 1

        self.hash_table[index] = key, value, hash(key)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.find_index(key)

        if not self.hash_table[index]:
            raise KeyError(
                f"There is no key/value pair assigned to key: '{key}'"
            )

        return self.hash_table[index][1]

    def __delitem__(self, key: Hashable) -> None:
        index = self.find_index(key)

        if not self.hash_table[index][1]:
            pass

        self.hash_table[index] = (None, None, self.hash_table[index][2])
        self.length - 1

    def clear(self) -> None:
        self.__init__()

    def __len__(self) -> int:
        return self.length
