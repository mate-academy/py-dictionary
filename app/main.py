from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.initial_size = 8
        self.length = 0
        self.hash_table = [[]] * self.initial_size

    def resize(self) -> None:
        hash_table_to_resize = self.hash_table
        self.initial_size *= 2
        self.hash_table = [[]] * self.initial_size
        self.length = 0
        for node in hash_table_to_resize:
            if node:
                key, value, hash_ = node
                self.__setitem__(key, value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length > int(self.initial_size * (2 / 3)):
            self.resize()
        index = hash(key) % self.initial_size
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = key, value, hash(key)
                self.length += 1
                break
            if (key == self.hash_table[index][0]
                    and hash(key) == self.hash_table[index][2]):
                self.hash_table[index] = key, value, hash(key)
                break
            else:
                index = (index + 1) % self.initial_size

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.initial_size
        while self.hash_table[index]:
            if (hash(key) == self.hash_table[index][2]
                    and key == self.hash_table[index][0]):
                return self.hash_table[index][1]
            index = (index + 1) % self.initial_size
        raise KeyError

    def __len__(self) -> int:
        return self.length
