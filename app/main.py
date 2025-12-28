from typing import Any


class Dictionary:

    def __init__(self,) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length + 1 > self.capacity * (2 / 3):
            self.resize()
        hash_key = hash(key)
        index = self.get_index(hash_key)

        while self.hash_table[index]:
            if key == self.hash_table[index][0]:
                self.hash_table[index][2] = value
                return
            index += 1
            if index == len(self.hash_table):
                index = 0
        self.hash_table[index] = [key, hash_key, value]
        self.length += 1

    def __getitem__(self, key: Any) -> Any:

        hash_key = hash(key)
        index = self.get_index(hash_key)

        while self.hash_table[index]:
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_key):
                return self.hash_table[index][2]
            index += 1
            if index == len(self.hash_table):
                index = 0

        raise KeyError

    def __len__(self) -> int:
        return self.length

    def get_index(self, hash_key: int) -> int:
        return hash_key % self.capacity

    def resize(self) -> None:

        self.length = 0
        self.capacity *= 2
        new_list = [[] for _ in range((len(self.hash_table) * 2))]
        hash_list_copy = self.hash_table
        self.hash_table = new_list
        for item in hash_list_copy:
            if item:
                self.__setitem__(item[0], item[2])
