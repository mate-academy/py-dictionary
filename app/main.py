from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.size = 8
        self.hash_table = [None] * self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length > int(self.size * 2 / 3):
            self.resize()
        hashed = hash(key)
        index = hashed % self.size
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, value, hashed]
                self.length += 1
                break
            elif self.hash_table[index][0] == key and \
                    self.hash_table[index][2] == hashed:
                self.hash_table[index][1] = value
                break
            else:
                index = (index + 1) % self.size

    def __getitem__(self, key: Any) -> Any:
        hashed = hash(key)
        index = hashed % self.size
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.size
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.size *= 2
        self.length = 0
        old_table = self.hash_table
        self.hash_table = [None] * self.size
        for items in old_table:
            if items:
                self.__setitem__(items[0], items[1])
