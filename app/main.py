from typing import Any


class Dictionary:
    def __init__(self, *args) -> None:
        self.args = args
        self.hash_table = []
        self.memory_size = 8
        self.dict_size = 0
        while len(args) > self.memory_size * 2 / 3:
            self.memory_size *= 2

        for _ in range(self.memory_size):
            self.hash_table.append([])

        for couple in self.args:
            self.__setitem__(couple[0], couple[1])

    def __setitem__(self, key: Any, value: Any) -> None:
        for slot in self.hash_table:
            if len(slot) == 3 and slot[0] == key:
                slot[2] = value
                return

        if self.__len__() >= self.get_load_factor():
            self.memory_size *= 2
            table = self.hash_table
            self.hash_table = []
            self.dict_size = 0

            for _ in range(self.memory_size):
                self.hash_table.append([])

            for slot in table:
                if len(slot) == 3:
                    self.__setitem__(slot[0], slot[2])

        memo_index = hash(key) % self.memory_size

        if len(self.hash_table[memo_index]) == 0:
            self.hash_table[memo_index] = ([key, hash(key), value])
            self.dict_size += 1
        else:
            for node in (self.hash_table[memo_index + 1:]
                         + self.hash_table[:memo_index]):
                if len(node) == 0:
                    node.extend([key, hash(key), value])
                    self.dict_size += 1
                    break

    def __getitem__(self, key: Any) -> Any:
        for slot in self.hash_table:
            if len(slot) == 3 and slot[0] == key:
                return slot[2]
        raise KeyError("Wrong key")

    def __len__(self) -> int:
        return self.dict_size

    def get_load_factor(self) -> int:
        return int(self.memory_size * 2 / 3)
