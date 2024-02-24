from typing import Any, Hashable


BLANK = object()


class Node:
    def __init__(
            self, key: Hashable,
            node_hash: int,
            value: Any
    ) -> None:
        self.key = key
        self.node_hash = node_hash
        self.value = value


class Dictionary:
    def __init__(self, table_size: int = 8) -> None:
        self.table_size = table_size
        self.number_of_elements = 0
        self.hash_table = self.table_size * [BLANK]

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        Dictionary.key_type_check(key)

        if self.number_of_elements > self.table_size * (2 / 3):
            self.resize(self.table_size * 2)

        index = hash(key) % self.table_size

        while (self.hash_table[index] is not BLANK
               and self.hash_table[index].key != key):
            index = (index + 1) % self.table_size

        if self.hash_table[index] is BLANK:
            self.number_of_elements += 1

        self.hash_table[index] = Node(
            key=key,
            node_hash=hash(key),
            value=value)

    def __getitem__(
            self,
            key: Hashable,
    ) -> Any | None:
        Dictionary.key_type_check(key)

        index = hash(key) % self.table_size

        while self.hash_table[index] is not BLANK:
            if self.hash_table[index].key == key:
                return self.hash_table[index].value
            index = (index + 1) % self.table_size

        raise KeyError(f"There is no item with key: {key}")

    def resize(self, new_table_size: int) -> None:
        new_hash_table = new_table_size * [BLANK]

        for index in range(self.table_size):
            if self.hash_table[index] is not BLANK:
                key = self.hash_table[index].key
                value = self.hash_table[index].value
                new_index = hash(self.hash_table[index].key) % new_table_size
                while new_hash_table[new_index] is not BLANK:
                    new_index = (new_index + 1) % new_table_size

                new_hash_table[new_index] = Node(
                    key=key,
                    node_hash=hash(key),
                    value=value)

        self.hash_table = new_hash_table
        self.table_size = new_table_size

    def __len__(self) -> int:
        return self.number_of_elements

    @staticmethod
    def key_type_check(key: Any) -> None:
        try:
            hash(key)
        except TypeError:
            print(f"Unhashable type: '{type(key).__name__}'")
            raise
