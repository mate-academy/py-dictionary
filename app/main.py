from typing import Any, Hashable


class Dictionary:

    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.length = 0
        self.hash_table = [None] * 8
        self.capacity = len(self.hash_table)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        new_key_hash, index = self.count_index(key)

        while self.hash_table[index]:
            table_key, _, _ = self.hash_table[index]
            if table_key == key:
                self.hash_table[index] = (key, new_key_hash, value)
                return
            index = (index + 1) % self.capacity

        self.length += 1
        self.hash_table[index] = (key, hash(key), value)
        self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        _, index = self.count_index(key)

        while self.hash_table[index]:
            table_key, _, value = self.hash_table[index]
            if table_key == key:
                return value
            index = (index + 1) % self.capacity

        raise KeyError

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        threshold = self.capacity * Dictionary.LOAD_FACTOR

        if self.length <= threshold:
            return

        self.capacity *= 2
        old_dictionary = self.hash_table

        self.hash_table = [None] * self.capacity
        self.length = 0

        [self.__setitem__(element[0], element[2])
         for element in old_dictionary
         if element]

    def count_index(self, new_key: Hashable) -> tuple:
        new_key_hash = hash(new_key)
        return new_key_hash, new_key_hash % self.capacity
