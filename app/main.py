from typing import Any, Hashable
from fractions import Fraction


class Node:
    def __init__(self, key: Hashable, key_hash: int, value: Any) -> None:
        self.key = key
        self.key_hash = key_hash
        self.value = value


class Dictionary:
    load_factor = Fraction(2, 3)

    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:

        if self.length >= round(self.capacity * self.load_factor):
            self.__hash_table_resize()

        self.__put_key_value_to_a_hash_table(key, value)

    def __put_key_value_to_a_hash_table(
        self,
        key: Hashable,
        value: Any,
        ignore_counter_of_length: bool = False
    ) -> None:

        index_in_hash_table = self.__find_index(key)
        cell = self.hash_table[index_in_hash_table]
        if not cell:
            self.hash_table[index_in_hash_table] = (
                Node(key=key, key_hash=hash(key), value=value)
            )

            if not ignore_counter_of_length:
                self.length += 1
        else:
            cell.value = value

    def __find_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (
                self.hash_table[index] is not None
                and key != self.hash_table[index].key
        ):
            index = (index + 1) % self.capacity
        print(index)
        return index

    def __hash_table_resize(self) -> None:
        template_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for items in template_hash_table:
            if items:
                self.__put_key_value_to_a_hash_table(
                    items.key,
                    items.value,
                    ignore_counter_of_length=True
                )

    def __getitem__(self, key: Hashable) -> Any:
        index_in_hash_table = self.__find_index(key)
        if not self.hash_table[index_in_hash_table]:
            raise KeyError("No such key found in this dictionary")
        return self.hash_table[index_in_hash_table].value

    def __len__(self) -> int:
        return self.length

    def __delitem__(self, key: Hashable) -> None:
        index_in_hash_table = self.__find_index(key)
        if self.hash_table[index_in_hash_table] is None:
            raise KeyError("No such key found in this dictionary")

        self.hash_table[index_in_hash_table] = None
        self.length -= 1
