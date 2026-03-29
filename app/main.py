from typing import Any, Hashable
from copy import deepcopy


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.hash_table: list[tuple] = [(None, None, None)] * self.capacity
        self.load_factor: float = 2 / 3
        self.items_number: int = 0

    def check_is_sell_empty(self, index: int) -> bool:
        return self.hash_table[index][0] is None

    @staticmethod
    def validate_key(key: Any) -> None:
        if not isinstance(key, Hashable):
            raise KeyError("Invalid type for the Dictionary key")

    def check_is_the_same_key(self, new_key: Hashable,
                              index: int) -> bool:
        return self.hash_table[index][0] == new_key

    def get_item_index_and_status(self, key: Hashable,
                                  key_hash: int) -> (int, bool):
        index = key_hash % self.capacity
        attempts = 0

        while True:
            if attempts == self.capacity:
                raise KeyError("Infinite loop")

            attempts += 1

            if self.check_is_sell_empty(index):
                return index, True

            if self.check_is_the_same_key(key, index):
                return index, False

            if index < (len(self.hash_table) - 1):
                index += 1
            else:
                index = 0

    def put_item_to_hash_table(self, key: Hashable,
                               value: Any) -> bool:
        key_hash = hash(key)
        index, is_new = self.get_item_index_and_status(key, key_hash)

        self.hash_table[index] = (key, key_hash, value)

        return is_new

    def resize(self) -> None:
        self.capacity *= 2
        hash_table_copy = deepcopy(self.hash_table)

        self.hash_table = [(None, None, None)] * self.capacity

        for element in hash_table_copy:
            if not element[0] is None:
                self.put_item_to_hash_table(element[0], element[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        Dictionary.validate_key(key)

        if self.capacity * self.load_factor < self.items_number + 1:
            self.resize()

        is_new = self.put_item_to_hash_table(key, value)

        if is_new:
            self.items_number += 1

    def __getitem__(self, key: Hashable) -> Any:
        Dictionary.validate_key(key)

        key_hash = hash(key)
        index = key_hash % self.capacity

        attempts = 0

        while True:
            if attempts == self.capacity:
                raise KeyError("Element with provided key doesn't exist")

            attempts += 1

            if self.check_is_the_same_key(key, index):
                return self.hash_table[index][2]

            if index < (len(self.hash_table) - 1):
                index += 1
            else:
                index = 0

    def __len__(self) -> int:
        return self.items_number
