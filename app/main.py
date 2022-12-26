from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = (self.capacity * 2 / 3) + 1
        self.length_table = 0
        self.hash_table = [None for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.threshold <= self.length_table:
            self.refresh_threshold()
        index = hash(key) % self.capacity
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = [key, value]
                self.length_table += 1
                break
            if self.hash_table[index][0] == key:
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def refresh_threshold(self) -> None:
        self.capacity *= 2
        self.length_table = 0
        self.threshold = (self.capacity * 2 / 3) + 1
        old_hash_table = self.hash_table
        self.hash_table = [None for _ in range(self.capacity)]
        for cell in old_hash_table:
            if cell:
                self.__setitem__(cell[0], cell[1])

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while True:
            if self.hash_table[index]:
                if self.hash_table[index][0] == key:
                    return self.hash_table[index][1]
            else:
                raise KeyError
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length_table
