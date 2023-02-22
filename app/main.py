from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 10,) -> None:
        self.capacity = capacity
        self.threshold = int(self.capacity * 0.75)
        self.size = 0
        self.table = [None] * self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * 0.75)
        self.size = 0
        old_table = self.table
        self.table = [None] * self.capacity
        for cell in old_table:
            if cell:
                self.__setitem__(cell[0], cell[1])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > self.threshold:
            self.resize()
        current_hash = hash(key)
        index = current_hash % self.capacity
        while True:
            if not self.table[index]:
                self.table[index] = [key, value, current_hash]
                self.size += 1
                break
            if (
                self.table[index][0] == key
                and self.table[index][2] == current_hash
            ):
                self.table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> None:
        current_hash = hash(key)
        index = current_hash % self.capacity
        while self.table[index]:
            if (
                self.table[index][2] == current_hash
                and self.table[index][0] == key
            ):
                return self.table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.size
