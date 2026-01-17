from dataclasses import dataclass
from typing import Any, Hashable


INITIAL_CAPACITY = 8
RESIZE_THRESHOLD = 2 / 3


@dataclass
class Node:
    key: Hashable
    value: Any

    def __repr__(self) -> str:
        key_string = f"'{self.key}'" if isinstance(self.key, str) else self.key
        value_string = \
            f"'{self.value}'" if isinstance(self.value, str) else self.value
        return f"{key_string}: {value_string}"


class Dictionary:
    def __init__(
            self,
            capacity: int = INITIAL_CAPACITY,
            load_factor: float = RESIZE_THRESHOLD
    ) -> None:
        self.length = 0
        self.capacity = capacity
        self.load_factor = load_factor
        self.hash_table: list[Node | None] = [None] * self.capacity

    def __str__(self) -> str:
        presentation = "{"
        for el in self.hash_table:
            if el:
                presentation += f"{el}, "
        presentation = presentation.strip(", ") + "}"
        return presentation + "___" + str(self.hash_table)

    def calculating_index(self, key: Hashable) -> int:
        index = hash(key) % self.capacity

        while (
                self.hash_table[index] is not None
                and self.hash_table[index].key != key
        ):
            index = (index + 1) % self.capacity
        return index

    def extend_hash_table(self) -> None:
        old_hash_table = self.hash_table
        self.capacity = self.capacity * 2
        self.hash_table = [None] * self.capacity

        for node in old_hash_table:
            if node is not None:
                index = self.calculating_index(node.key)
                self.hash_table[index] = node

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length + 1 >= self.capacity * self.load_factor:
            self.extend_hash_table()

        index = self.calculating_index(key)

        if self.hash_table[index] is not None:
            if self.hash_table[index].key == key:
                self.hash_table[index].value = value
                return
            else:
                for index, el in enumerate(self.hash_table):
                    if el and el.key == key:
                        self.hash_table[index].value = value
                        return

        self.length += 1
        self.hash_table[index] = Node(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity

        if (
                self.hash_table[index] is not None
                and self.hash_table[index].key == key
        ):
            return self.hash_table[index].value

        for index, el in enumerate(self.hash_table):
            if el and el.key == key:
                return self.hash_table[index].value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.length
