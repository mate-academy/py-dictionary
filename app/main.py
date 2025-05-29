from typing import Hashable


class Dictionary:

    def __init__(self) -> None:
        self.table = [[] for _ in range(8)]
        self.length = 8
        self.size = 0

    def __setitem__(self, key: Hashable, value: any) -> None:
        index = self.index_function(key)

        if self.table[index]:
            while True:
                ls = self.table[index]

                if not ls or key == ls[0]:
                    self.size += not ls
                    self.table[index] = [key, value]
                    break
                else:
                    index += 1
                    if index >= self.length:
                        index = 0
        else:
            self.table[index] = [key, value]
            self.size += 1
        self.check_size()

    def __getitem__(self, key: Hashable) -> list:
        index = self.index_function(key)

        if self.table[index]:
            while True:
                ls = self.table[index]
                if not ls:
                    break
                if ls[0] == key:
                    return ls[1]

                index += 1
                if index >= len(self.table):
                    index = 0
        raise KeyError("Key not found")

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.__init__()

    def index_function(self, key: Hashable) -> int:
        return hash(key) % self.length

    def check_size(self) -> None:
        if self.length * 2 / 3 < self.__len__():
            self.length *= 2
            new_table = [[] for _ in range(self.length)]

            for ls in self.table:
                if ls:
                    key = ls[0]
                    value = ls[1]

                    index = self.index_function(key)

                    while new_table[index]:
                        index += 1
                        if index >= self.length:
                            index = 0
                    new_table[index] = [key, value]

            self.table = new_table
