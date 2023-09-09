from app.node import Node
from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.hash_table = [None] * 8
        self.length = 0

    def resize(self) -> None:
        new_table = [None] * len(self.hash_table) * 2

        for element in self.hash_table:
            if element is None:
                continue

            element_number = element.hash % len(new_table)

            if new_table[element_number] is None:
                new_table[element_number] = element
                continue

            if new_table[element_number].key == element.key:
                new_table[element_number].value = element.value
                continue

            start_index = element_number - len(new_table) + 1
            end_index = len(new_table) + start_index - 2
            for element_index in range(start_index, end_index):
                if new_table[element_index] is None:
                    new_table[element_index] = element
                    break

                if new_table[element_index].key == element.key:
                    new_table[element_index].value = element.value
                    break

        self.hash_table = new_table

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        self.length += 1

        if self.length > (2 / 3 * len(self.hash_table)):
            self.resize()

        element = Node(
            key,
            hash(key),
            value
        )

        element_number = element.hash % len(self.hash_table)

        if self.hash_table[element_number] is None:
            self.hash_table[element_number] = element
            return

        if self.hash_table[element_number].key == key:
            self.hash_table[element_number].value = value
            self.length -= 1
            return

        start_index = element_number - len(self.hash_table) + 1
        end_index = len(self.hash_table) + start_index - 2
        for element_index in range(start_index, end_index):
            if self.hash_table[element_index] is None:
                self.hash_table[element_index] = element
                return

            if self.hash_table[element_index].key == key:
                self.hash_table[element_index].value = value
                self.length -= 1
                return

    def __getitem__(self, item: Hashable) -> Any:
        element_number = hash(item) % len(self.hash_table)

        if self.hash_table[element_number] is None:
            raise KeyError(item)

        if self.hash_table[element_number].key == item:
            return self.hash_table[element_number].value

        start_index = element_number - len(self.hash_table) + 1
        end_index = len(self.hash_table) + start_index - 2
        for element_index in range(start_index, end_index):
            if self.hash_table[element_index] is None:
                raise KeyError(item)

            if self.hash_table[element_index].key == item:
                return self.hash_table[element_index].value

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        return str(self.hash_table)
