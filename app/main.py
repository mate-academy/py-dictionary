from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.initial_capacity = 8
        self.load_factor = 0.6
        self.hash_table = [[] for _ in range(self.initial_capacity)]
        self.size = 0

    def resize(self) -> None:
        old_table = self.hash_table
        self.initial_capacity *= 2
        self.size = 0
        self.hash_table = [[] for _ in range(self.initial_capacity)]
        for table in old_table:
            if table:
                key, value, hash_value = table
                self.__setitem__(key, value)

    def __setitem__(self, key: Hashable, value: Hashable) -> None:
        if self.size > int(self.initial_capacity * self.load_factor):
            self.resize()
        hash_value = hash(key)
        index = hash_value % self.initial_capacity
        while len(self.hash_table[index]) == 3:
            if self.hash_table[index][0] == key:
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.initial_capacity
        else:
            self.hash_table[index] = [key, value, hash_value]
            self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index = hash_value % self.initial_capacity
        while len(self.hash_table[index]) == 3:
            if (
                    hash_value == self.hash_table[index][-1]
            ) and (
                    self.hash_table[index][0] == key
            ):
                return self.hash_table[index][1]
            index = (index + 1) % self.initial_capacity
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.initial_capacity = 8
        self.hash_table = [[] for _ in range(self.initial_capacity)]
        self.size = 0

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.initial_capacity
        while len(self.hash_table[index]) == 3:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = []
                self.size -= 1
            break
