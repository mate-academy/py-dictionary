from typing import Any


class Dictionary:
    CAPACITY = 8
    lenght = 0

    def __init__(self) -> None:
        self.hash_table: list = [None] * 8

    def resize(self) -> None:
        self.CAPACITY *= 2
        self.resize_table = self.hash_table
        self.hash_table = [None] * self.CAPACITY
        self.lenght = 0
        for item in self.resize_table:
            if item is not None:
                self.__setitem__(item.key, item.value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.lenght >= self.CAPACITY * 2 // 3:
            self.resize()

        element = Node(key, value)
        index = element._hash % self.CAPACITY
        while True:
            if index == len(self.hash_table):
                index = 0
                continue
            if self.hash_table[index] is None:
                self.lenght += 1
                self.hash_table[index] = element
                break
            if self.hash_table[index].key == key:
                self.hash_table[index] = element
                break
            else:
                index += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.CAPACITY
        while True:
            if index == len(self.hash_table):
                index = 0
                continue
            if self.hash_table[index] is None:
                raise KeyError
            if (self.hash_table[index]._hash == hash(key)
                    and self.hash_table[index].key == key):
                return self.hash_table[index].value
            index += 1

    def __len__(self) -> int:
        return self.lenght

    def __delitem__(self, key: Any) -> None:
        count = self.CAPACITY
        index = hash(key) % self.CAPACITY
        while True:
            if index == len(self.hash_table):
                index = 0
                continue
            if count == 0:
                raise KeyError

            if self.hash_table[index] is not None:
                if (self.hash_table[index]._hash == hash(key)
                        and self.hash_table[index].key == key):
                    self.hash_table[index] = None
                    self.lenght -= 1
                    break
            index += 1
            count -= 1


class Node:
    def __init__(self, key: Any, value: Any) -> None:
        self._hash = hash(key)
        self.key = key
        self.value = value
