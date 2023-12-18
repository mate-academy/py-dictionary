from copy import deepcopy
from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.capacity = 8

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Any:
        return self

    def __setitem__(self,
                    key: int | float | str | bool | tuple,
                    value: int | float | str | bool | tuple
                    ) -> None | str:
        if type(key) is list | dict | set:
            return f"Key parameter {key} is not acceptable"

        hash_key = hash(key)
        index_table = hash_key % self.capacity

        if self.hash_table[index_table] is None:
            self.save_dict_element(key, value, hash_key, index_table)
            self.check_change_capacity()
        else:
            if self.check_exist_key(key) is False:
                while True:
                    if ((self.hash_table[index_table] is None)
                       or (self.hash_table[index_table] == -1)):
                        self.save_dict_element(key, value,
                                               hash_key, index_table)
                        self.check_change_capacity()
                        break
                    index_table += 1
                    if index_table == self.capacity:
                        index_table = 0

            else:
                while True:
                    if ((self.hash_table[index_table] != -1)
                            and (self.hash_table[index_table][0] == hash_key)
                            and (self.hash_table[index_table][1] == key)):
                        self.hash_table[index_table][2] = value
                        break
                    index_table += 1
                    if index_table == self.capacity:
                        index_table = 0

    def __getitem__(self, key: int | float | str | bool | tuple) -> Any:
        index_table = self.search_index_element(key)

        return self.hash_table[index_table][2]

    def search_index_element(self,
                             key: int | float | str | bool | tuple
                             ) -> int | str:
        hash_key = hash(key)
        index_table = hash_key % self.capacity
        while True:
            if self.hash_table[index_table] is None:
                raise KeyError(f"Key: {key} is not in dictionary.")
            if ((self.hash_table[index_table] != -1)
                    and (self.hash_table[index_table][0] == hash_key)
                    and (self.hash_table[index_table][1] == key)):
                return index_table
            index_table += 1
            if index_table == self.capacity:
                index_table = 0

    def check_exist_key(self,
                        key: int | float | str | bool | tuple
                        ) -> bool:
        hash_key = hash(key)
        index_table = hash_key % self.capacity
        while True:
            if self.hash_table[index_table] is None:
                return False
            if ((self.hash_table[index_table] != -1)
                and (self.hash_table[index_table][0] == hash_key)
                    and (self.hash_table[index_table][1] == key)):
                return True
            index_table += 1
            if index_table == self.capacity:
                index_table = 0

    def __delitem__(self,
                    key: int | float | str | bool | tuple
                    ) -> None:
        index_table = self.search_index_element(key)
        self.length -= 1
        self.hash_table[index_table] = -1

    def save_dict_element(self,
                          key: int | float | str | bool | tuple,
                          value: int | float | str | bool | tuple,
                          hash_key: int,
                          index_table: int
                          ) -> None:
        self.hash_table[index_table] = [-1, None, None]
        self.hash_table[index_table][0] = hash_key
        self.hash_table[index_table][1] = key
        self.hash_table[index_table][2] = value
        self.length += 1

    def check_change_capacity(self) -> None:
        if self.length >= self.capacity * 2 // 3:
            self.capacity *= 2
            new_dict = Dictionary()
            new_dict.hash_table = [None] * self.capacity
            new_dict.capacity = self.capacity
            for bucket in self.hash_table:
                if bucket is not None and bucket != -1:
                    new_dict.__setitem__(bucket[1], bucket[2])
            self.hash_table = deepcopy(new_dict.hash_table)

    def get(self,
            key: int | float | str | bool | tuple
            ) -> Any:
        return self.__getitem__(key)

    def pop(self,
            key: int | float | str | bool | tuple
            ) -> Any:
        deleting_object = deepcopy(self.__getitem__(key))
        self.__delitem__(key)
        return deleting_object

    def update(self,
               key: int | float | str | bool | tuple,
               value: int | float | str | bool | tuple
               ) -> None:
        self.__setitem__(key, value)

    def clear(self) -> None:
        self.length = 0
        self.hash_table: list = [None] * 8
        self.capacity = 8
