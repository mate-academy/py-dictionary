from dataclasses import dataclass
from typing import Any
from collections.abc import Hashable


@dataclass
class Node:
    key: Hashable
    value: Any
    hash_node: int


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table = [None for _ in range(8)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        capacity = len(self.hash_table)
        hash_key = hash(key)
        node = Node(key, value, hash_key)
        if len(self) >= int(capacity * (2 / 3)):
            new_hash_table = [None for _ in range(capacity * 2)]
            new_capacity = len(new_hash_table)
            self.length = 0
            self.resize_hash_table(key, value, new_capacity, new_hash_table)
            index_item = hash_key % new_capacity
            self.save_item_in_table(
                new_hash_table,
                new_capacity,
                index_item,
                node,
                key,
                value)
            self.hash_table = new_hash_table
            return
        index_item = hash_key % capacity
        self.save_item_in_table(
            self.hash_table,
            capacity,
            index_item,
            node,
            key,
            value)

    def resize_hash_table(
            self,
            key: Hashable,
            value: Any,
            new_capacity: int,
            new_hash_table: list) -> None:
        for item in self.hash_table:
            if isinstance(item, Node):
                initial_index = item.hash_node % new_capacity
                if new_hash_table[initial_index] is None:
                    new_hash_table[initial_index] = item
                    self.length += 1
                    continue
                if new_hash_table[initial_index].key == item.key:
                    new_hash_table[initial_index].value = value
                    continue
                if new_hash_table[initial_index].key != item.key:
                    last_index = initial_index
                    item_hash = item.hash_node
                    while True:
                        example = (5 * last_index + 1 + item_hash)
                        curent_index = example % new_capacity
                        last_index = curent_index
                        item_hash = item_hash >> 5
                        if new_hash_table[curent_index] is None:
                            new_hash_table[curent_index] = item
                            self.length += 1
                            break
                        if new_hash_table[curent_index].key == key:
                            new_hash_table[curent_index].value = item.value
                            break

    def find_index_and_get_item(
            self,
            key: Hashable,
            capacity: int,
            hash_key: int) -> Any:
        initial_index = hash_key % capacity
        item = self.hash_table[initial_index]
        if item is None:
            raise KeyError(f"Key '{key}' not found")
        if item.key == key:
            return item.value
        if item.key != key:
            perturb = hash(key)
            last_index = initial_index
            while True:
                current_index = (5 * last_index + 1 + perturb) % capacity
                last_index = current_index
                perturb = perturb >> 5
                if self.hash_table[current_index] is None:
                    raise KeyError(f"Key '{key}' not found")
                if self.hash_table[current_index].key == key:
                    return self.hash_table[current_index].value

    def __getitem__(self, key: Hashable) -> Any:
        capacity = len(self.hash_table)
        hash_key = hash(key)
        return self.find_index_and_get_item(
            key,
            capacity,
            hash_key)

    def __len__(self) -> Any:
        return self.length

    def save_item_in_table(
            self,
            table_to_save: list,
            capacity: int,
            index_item: int,
            node: Node,
            key: Hashable,
            value: Any) -> None:
        if table_to_save[index_item] is None:
            table_to_save[index_item] = node
            self.length += 1
            return
        if table_to_save[index_item].key == key:
            table_to_save[index_item].value = value
            return
        if table_to_save[index_item].key != key:
            perturb = hash(key)
            last_index = index_item
            while True:
                base_index = (5 * last_index + 1 + perturb)
                current_index = base_index % capacity
                last_index = current_index
                perturb = perturb >> 5
                if table_to_save[current_index] is None:
                    table_to_save[current_index] = node
                    self.length += 1
                    break
                if table_to_save[current_index].key == key:
                    table_to_save[current_index].value = value
                    break
