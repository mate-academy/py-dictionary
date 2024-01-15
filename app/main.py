from __future__ import annotations
from typing import Any, Hashable


class Node:

    def __init__(self, key: Hashable, value: Any) -> None:
        self._key = key
        self._value = value
        self.hash = hash(self)

    def get_key(self) -> Hashable:
        return self._key

    def get_value(self) -> Any:
        return self._value

    def set_value(self, value: Any) -> None:
        self._value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Node):
            if self._key == other.get_key():
                return True
        return self.hash == (hash(other))

    def __hash__(self) -> int:
        return hash(self._key)

    def __repr__(self) -> str:
        return str(self._value)


class Dictionary:

    def __init__(self) -> None:
        self.lentgh = 0
        self.capacity = 8
        self.hash_table = self.make_hash_table()
        self.keys = []

    def items(self) -> list[tuple[Hashable, Any]]:
        items = []
        for node in self.hash_table:
            if node:
                items.append((node.get_key(), node.get_value()))
        return items

    def __repr__(self) -> str:
        str_dict = ""
        for key, value in self.items():
            if isinstance(key, str):
                str_dict += f"'{key}': {value}, "
            else:
                str_dict += f"{key}: {value}, "

        return "{" + str_dict[:-2] + "}"

    def __len__(self) -> int:
        return self.lentgh

    @staticmethod
    def make_hash_table(lentgh: int = 8) -> list[None]:
        hash_table = []
        for i in range(lentgh):
            hash_table.append(None)
        return hash_table

    def find_index_for_new(
            self,
            node: Node,
            key: Hashable,
            index: int
    ) -> None:

        if self.lentgh == int(self.capacity * 2 / 3):
            self.resize()
            self[key] = node.get_value()
            return

        if not self.hash_table[index]:
            self.hash_table[index] = node
            self.keys.append(key)
            self.lentgh += 1
            return

        for index in range(self.capacity):
            if not self.hash_table[index]:
                self.hash_table[index] = node
                self.keys.append(key)
                self.lentgh += 1
                return

    def find_index_for_old(
            self,
            key: Hashable,
            value: Any,
            index: int
    ) -> None:

        if self.hash_table[index] and self.hash_table[index].get_key() == key:
            return self.hash_table[index].set_value(value)

        for index in range(self.capacity):
            element = self.hash_table[index]
            if element and element.get_key() == key:
                self.hash_table[index].set_value(value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if isinstance(key, (dict, list)):
            raise ValueError(f"Не можна задавати такий ключ - "
                             f"[{type(key)}] для словника")

        node = Node(key, value)
        index = node.hash % self.capacity

        if key not in self.keys:
            return self.find_index_for_new(node, key, index)
        self.find_index_for_old(key, value, index)

    def __getitem__(self, key: Hashable) -> Any:
        if key not in self.keys:
            raise KeyError(f"Немає такого ключа - [{key}] в словнику")

        node = Node(key, None)
        index = node.hash % self.capacity
        if self.hash_table[index] and self.hash_table[index].get_key() == key:
            return self.hash_table[index].get_value()

        for index in range(self.capacity):
            if self.hash_table[index].get_key() == key:
                return self.hash_table[index].get_value()

    def resize(self) -> None:
        temp_hash_table = self.hash_table.copy()

        self.hash_table = self.make_hash_table(self.capacity * 2)
        self.capacity *= 2
        self.keys = []
        self.lentgh = 0

        for node in temp_hash_table:
            if node:
                self[node.get_key()] = node.get_value()
