from dataclasses import dataclass
from collections.abc import Hashable
from typing import Any


@dataclass(slots=True)
class Node:
    key: Hashable
    value: Any
    hash_value: int


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.capacity = 8

    def resize(self) -> None:
        if self.length / self.capacity >= 2 / 3:
            new_table = [None] * (self.capacity * 2)
            self.capacity *= 2
            for item in self.hash_table:
                if item is not None:
                    new_address = item.hash_value % self.capacity
                    if new_table[new_address] is None:
                        new_table[new_address] = item
                    else:
                        found_place_in_table = False
                        while not found_place_in_table:
                            new_address = (new_address + 1) % self.capacity
                            if new_table[new_address] is not None:
                                continue
                            new_table[new_address] = item
                            found_place_in_table = True

            self.hash_table = new_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        address = key_hash % self.capacity
        item = self.hash_table[address]

        if item is None:
            self.hash_table[address] = Node(key, value, key_hash)
            self.length += 1

        elif item.hash_value == key_hash and item.key == key:
            item.value = value

        else:
            found_place_in_table = False
            while not found_place_in_table:
                address = (address + 1) % self.capacity
                item = self.hash_table[address]
                if item is not None:
                    if item.hash_value == key_hash and item.key == key:
                        item.value = value
                        break
                    else:
                        continue
                self.hash_table[address] = Node(key, value, key_hash)
                self.length += 1
                found_place_in_table = True
        self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        address = key_hash % self.capacity
        item = self.hash_table[address]
        if item is None:
            raise KeyError(f"Key {key!r} not found")
        if key_hash == item.hash_value and key == item.key:
            return item.value
        while True:
            address = (address + 1) % self.capacity

            item = self.hash_table[address]
            if item is None:
                raise KeyError(f"Key {key!r} not found")
            if (
                    key_hash == item.hash_value
                    and key == item.key
            ):
                return item.value

    def __len__(self) -> int:
        return self.length
