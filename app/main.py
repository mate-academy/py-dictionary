from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table = [[]] * self.capacity

    def resize(self) -> None:
        hash_table_to_resize = self.hash_table
        self.capacity *= 2
        self.hash_table = [[]] * self.capacity
        self.size = 0
        for node in hash_table_to_resize:
            if node:
                key, hash_, value = node
                self.__setitem__(key, value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > int(self.capacity * (2 / 3)):
            self.resize()
        index = hash(key) % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = key, hash(key), value
                self.size += 1
                break
            if (key == self.hash_table[index][0]
                    and hash(key) == self.hash_table[index][1]):
                self.hash_table[index] = key, hash(key), value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.hash_table[index]:
            if (hash(key) == self.hash_table[index][1]
                    and key == self.hash_table[index][0]):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.size
