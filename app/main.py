from typing import Any, Hashable
from copy import deepcopy


class Dictionary:
    class Node:
        def __init__(self, key: Hashable, value: Any, my_hash: int) -> None:
            self.key = key
            self.value = value
            self.my_hash = my_hash

        def __repr__(self) -> str:
            return f"Node(key={self.key}, value={self.value})"

    def __init__(self) -> None:
        self.__capacity = 8
        self.__load_factor = 0.667
        self.__size = 0
        self.__hash_table: list[None | Dictionary.Node] = [
            None for _ in range(self.__capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.__size >= self.__capacity * self.__load_factor:
            self.__resize()

        index = self.__find_index(key)
        if self.__hash_table[index] is None:
            self.__size += 1

        self.__hash_table[index] = Dictionary.Node(key, value, hash(key))

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__find_index(key)
        if self.__hash_table[index] is None:
            raise KeyError(f"Value for key '{key}' not found")

        return self.__hash_table[index].value

    def __delitem__(self, key: Hashable) -> None:
        index = self.__find_index(key)
        if self.__hash_table[index] is None:
            raise KeyError(f"Value for key '{key}' not found")

        self.__hash_table[index] = None
        self.__size -= 1

        for values in self.__hash_table:
            if values is not None:
                self.__setitem__(values.key, values.value)

    def __len__(self) -> int:
        return self.__size

    def __repr__(self) -> str:
        return str(self.__hash_table)

    def __find_index(self, key: Hashable) -> int:
        index = hash(key) % self.__capacity
        while (self.__hash_table[index] is not None
               and self.__hash_table[index].key != key):
            index = (index + 1) % self.__capacity

        return index

    def clear(self) -> None:
        self.__init__()

    def __resize(self) -> None:
        self.__capacity = self.__capacity * 2
        self.__size = 0
        copy_arr: list = deepcopy(self.__hash_table)
        self.__hash_table: list[None | Dictionary.Node] = [
            None for _ in range(self.__capacity)]

        for values in copy_arr:
            if values is not None:
                self.__setitem__(values.key, values.value)
