from __future__ import annotations

from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.capacity

    def __getitem__(self, input_key: Hashable) -> None:
        index = hash(input_key) % self.capacity
        while (self.hash_table[index]
               and self.hash_table[index][0] != input_key):
            index = (index + 1) % self.capacity
        if not self.hash_table[index]:
            raise KeyError(f"The Dictionary object doesn't contain element "
                           f"with key '{input_key}'")
        return self.hash_table[index][2]

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if len(self) == round(self.capacity * self.load_factor):
            self.resize()

        index = hash(key) % self.capacity

        while (self.hash_table[index] and self.hash_table[index][0] != key):
            index += 1
            if index > self.capacity - 1:
                index = 0
        self.hash_table[index] = (key, hash(key), value)

    def __len__(self) -> int:
        len_counter = 0
        for item in self.hash_table:
            if item:
                len_counter += 1
        return len_counter

    def __delitem__(self, key: Hashable) -> None:
        if key in self:
            for i in range(self.capacity):
                if self.hash_table[i] and self.hash_table[i][0] == key:
                    self.hash_table[i] = None
                    break
        else:
            raise KeyError(f"The Dictionary object doesn't contain element "
                           f"with key '{key}'")

    def resize(self) -> None:
        self.capacity *= 2
        old_hash_table_items = [item for item in self.hash_table if item]
        self.hash_table = [None] * self.capacity
        for key, _hash, value in old_hash_table_items:
            self[key] = value

    def get(self, input_key: Hashable) -> Any:
        for item in self.hash_table:
            if item and input_key == item[0]:
                return item[2]

    def clear(self) -> None:
        self.__init__()

    def update(self, other: Dictionary | dict | list | tuple | set) -> None:

        if isinstance(other, Dictionary):
            for item in other.hash_table:
                if item:
                    self[item[0]] = other[item[0]]

        elif (isinstance(other, list) or isinstance(other, tuple)
              or isinstance(other, set)):
            for item in other:
                if len(item) == 2:
                    self[item[0]] = item[1]
                else:
                    raise ValueError(f"Length of item {item} must be 2!")

        elif isinstance(other, dict):
            for key, value in other.items():
                self[key] = other[key]

        else:
            raise ValueError("Object to update must be "
                             "Dictionary, list, tuple or set!")

    def pop(self, key: Hashable, default: Any = None) -> Any:

        if self.get(key):
            for i in range(self.capacity):
                if self.hash_table[i] and self.hash_table[i][0] == key:
                    popped_value = self.hash_table[i]
                    self.hash_table[i] = None
                    return popped_value[2]

        elif default:
            return default

        raise KeyError(f"The Dictionary object doesn't contain element "
                       f"with key '{key}'. Add default value for return")
