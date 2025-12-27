from math import floor
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.load_factor = 0
        self.hash_table: list = []

    def get_table_place(self, key: Any) -> int:
        hashed_key = hash(key)
        table_place = round(hashed_key % len(self.hash_table))
        return table_place

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length == 0 or self.length >= self.load_factor:
            self.__resize__()
        table_place = self.get_table_place(key)
        while (self.hash_table[table_place] is not None
               and self.hash_table[table_place][0] != key
               and self.hash_table[table_place][0] != -1):
            table_place += 1
            table_place %= len(self.hash_table)
        if self.hash_table[table_place] is None:
            self.hash_table[table_place] = [key, hash(key), value]
            self.length += 1
        if (self.hash_table[table_place][0] == key
                or self.hash_table[table_place][0] != -1):
            self.hash_table[table_place][2] = value
            self.hash_table[table_place][1] = hash(key)

    def __getitem__(self, key: Any) -> Any:
        if len(self.hash_table) != 0:
            try:
                table_place = self.get_table_place(key)
                counter = 0
                while self.hash_table[table_place] is not None:
                    if counter > len(self.hash_table):
                        break
                    if self.hash_table[table_place][0] == key:
                        return self.hash_table[table_place][2]
                    table_place += 1
                    table_place %= len(self.hash_table)
                    counter += 1
            except KeyError("There is no such key in the list"):
                return -1
        else:
            raise KeyError("There is no such key in the list")

    def __len__(self) -> int:
        return self.length

    def __resize__(self) -> None:
        new_size = len(self.hash_table) + 8
        self.load_factor = floor(new_size * 2 / 3)
        list_to_rewrite = []
        self.length = 0
        for element in self.hash_table:
            if element is not None:
                list_to_rewrite.append(element)
        self.hash_table = [None] * new_size
        for element in list_to_rewrite:
            self.__setitem__(element[0], element[2])

    def clear(self) -> Any:
        self.hash_table = []
        return self.hash_table

    def __delitem__(self, key: Any) -> None:
        if len(self.hash_table) != 0:
            try:
                table_place = self.get_table_place(key)
                while self.hash_table[table_place] is not None:
                    if self.hash_table[table_place][0] == key:
                        self.hash_table[table_place] = None
                        self.length -= 1
                    table_place += 1
                    table_place %= len(self.hash_table)
            except KeyError:
                print("There is no such key in the list")
        else:
            raise KeyError("There is no such key in the list")

    def pop(self, key: Any) -> Any:
        if len(self.hash_table) != 0:
            try:
                table_place = self.get_table_place(key)
                while self.hash_table[table_place] is not None:
                    if self.hash_table[table_place][0] == key:
                        item_to_return = self.hash_table[table_place][2]
                        self.hash_table[table_place] = None
                        self.length -= 1
                        return item_to_return
                    table_place += 1
                    table_place %= len(self.hash_table)
            except KeyError("There is no such key in the list"):
                return 0
        else:
            raise KeyError("There is no such key in the list")

    def update(self, key: Any, value: Any) -> None:
        table_place = self.get_table_place(key)
        while (self.hash_table[table_place] is not None
               and self.hash_table[table_place][0] != key
               and self.hash_table[table_place][0] != -1):
            table_place += 1
            table_place %= len(self.hash_table)
        if (self.hash_table[table_place][0] == key
                or self.hash_table[table_place][0] != -1):
            self.hash_table[table_place][2] = value
            self.hash_table[table_place][1] = hash(key)

    def get(self, key: Any) -> Any:
        if len(self.hash_table) != 0:
            try:
                table_place = self.get_table_place(key)
                counter = 0
                while self.hash_table[table_place] is not None:
                    if counter > len(self.hash_table):
                        break
                    if self.hash_table[table_place][0] == key:
                        return self.hash_table[table_place][2]
                    table_place += 1
                    table_place %= len(self.hash_table)
                    counter += 1
            except KeyError("There is no such key in the list"):
                return None
        else:
            return None

    def __iter__(self) -> Any:
        for element in self.hash_table:
            if element is not None:
                yield element
