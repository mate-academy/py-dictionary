from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    key: Any
    value: Any
    hashed_key: int


class Dictionary:
    def __init__(self) -> None:
        self.lenght = 0
        self.hash_table = [None for i in range(0, 8)]

    def __len__(self) -> int:
        count = 0
        for element in self.hash_table:
            if element is not None:
                count += 1
        self.lenght = count
        return self.lenght

    def __setitem__(self, key: Any = None, value: Any = None) -> None:
        free_cells = self.hash_table.count(None)
        load_factor = round(len(self.hash_table) * (2 / 3))
        old_hash_table = self.hash_table

        def add_element(
                key_el: Any, value_el: Any, current_hash_table: list
        ) -> None:
            hashed_key = hash(key_el)
            index = hashed_key % len(current_hash_table)
            if (
                (current_hash_table[index] is not None)
                and (current_hash_table[index].key == key_el)
            ):
                current_hash_table[index].value = value_el
                return current_hash_table
            while ((current_hash_table[index] is not None)
                   and (current_hash_table[index].key != key_el)):
                index += 1
                if index >= len(current_hash_table):
                    index = 0
            current_hash_table[index] = Node(
                key=key_el, value=value_el, hashed_key=hashed_key
            )
            return current_hash_table

        if (len(old_hash_table) - free_cells) >= load_factor:
            self.hash_table = [
                None for i in range(0, (len(old_hash_table) * 2))
            ]
            for element in old_hash_table:
                if element is not None:
                    add_element(element.key, element.value, self.hash_table)
        add_element(key, value, self.hash_table)

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % len(self.hash_table)
        if self.hash_table[index] is None:
            raise KeyError(f"Such key '{key}' doesn't exist")
        if (
            (self.hash_table[index] is not None)
            and (self.hash_table[index].key == key)
        ):
            return self.hash_table[index].value
        new_index = index
        while ((self.hash_table[index] is not None)
               and (self.hash_table[index].key != key)):
            new_index += 1
            if new_index >= len(self.hash_table):
                new_index = 0
            if new_index == index:
                break
            if (
                (self.hash_table[new_index] is not None)
                and (self.hash_table[new_index].key == key)
            ):
                return self.hash_table[new_index].value
        raise KeyError(f"Such key '{key}' doesn't exist")

    def get(self, key: Any, defaul_value: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return defaul_value

    def clear(self) -> "Dictionary":
        self.hash_table = []
        return self.hash_table
