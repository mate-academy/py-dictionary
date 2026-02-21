from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.current = 0
        self.length = 0
        self.len_hash_table = 8
        self.hash_table: list = [None] * self.len_hash_table

    def resize(self) -> None:
        if int(self.len_hash_table * (2 / 3)) < self.length:
            old_length = self.length
            self.len_hash_table *= 2
            copy_hash_table = self.hash_table.copy()
            self.hash_table: list = [None] * self.len_hash_table
            for key_value in copy_hash_table:
                if key_value:
                    self.__setitem__(key_value[0], key_value[2])
            self.length = old_length

    def hash_function(self, key: Any) -> int:
        return hash(key) % self.len_hash_table

    def get_index_hash(self, key: Any) -> tuple[int, bool]:
        index_hash = self.hash_function(key)
        non_hash = index_hash
        non_bool = True
        current_count = 0
        while True:
            if current_count == self.len_hash_table:
                return non_hash, False
            elif self.hash_table[index_hash] is None:
                if non_bool:
                    non_hash = index_hash
                    non_bool = False
                index_hash = (index_hash + 1) % self.len_hash_table
                current_count += 1
            elif (self.hash_table[index_hash][0] == key
                  and self.hash_table[index_hash][1] == hash(key)):
                return index_hash, True
            else:
                index_hash = (index_hash + 1) % self.len_hash_table
                current_count += 1

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        try:
            index_hash = self.get_index_hash(key)
            self.hash_table[index_hash[0]] = [key, hash(key), value]
            if not index_hash[1]:
                self.length += 1
                self.resize()
        except TypeError:
            raise TypeError("unhashable type: 'list'")

    def __getitem__(self, key: Any) -> Any:
        try:
            index_hash = self.get_index_hash(key)
            if not index_hash[1]:
                raise KeyError(key)
            return self.hash_table[index_hash[0]][2]
        except TypeError:
            raise TypeError("unhashable type: 'list'")

    def update(self, *arg, **kwarg) -> None:
        if arg and isinstance(arg[0], list):
            for item in arg[0]:
                self.__setitem__(item[0], item[1])
        elif arg and isinstance(arg[0], dict):
            for key in arg[0]:
                self.__setitem__(key, arg[0][key])
        if kwarg:
            for key in kwarg:
                self.__setitem__(key, kwarg[key])

    def __str__(self) -> str:
        elements = []
        for item in self.hash_table:
            if item:
                elements.append(f"'{item[0]}': {item[2]}")
        return "{" + ", ".join(elements) + "}"

    def __iter__(self) -> Any:
        self.current = 0
        return self

    def __next__(self) -> Any:
        while True:
            if self.current < self.len_hash_table:
                value = self.hash_table[self.current]
                if value:
                    self.current += 1
                    return value[0]
                self.current += 1
            else:
                raise StopIteration

    def __delitem__(self, key: Any) -> None:
        index_hash = self.get_index_hash(key)
        if index_hash[1]:
            self.hash_table[index_hash[0]] = None
            self.length -= 1
        else:
            raise KeyError(key)

    def clear(self) -> None:
        self.current = 0
        self.length = 0
        self.len_hash_table = 8
        self.hash_table: list = [None] * self.len_hash_table
