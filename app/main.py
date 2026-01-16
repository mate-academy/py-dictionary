from typing import Hashable, Any


class Dictionary:
    initial_capacity = 8
    load_factor = 2 / 3

    def __init__(self) -> None:
        self.capacity = self.initial_capacity
        self.threshold = int(self.capacity * self.load_factor)
        self.table = [None] * self.capacity
        self.length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self.resize()

        index = hash(key) % self.capacity

        while True:
            if not self.table[index]:
                self.table[index] = [key, hash(key), value]
                self.length += 1
                break
            if self.table[index][0] == key:
                self.table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity

        while True:
            if self.table[index]:
                if self.table[index][0] == key:
                    return self.table[index][2]
                index = (index + 1) % self.capacity
                continue
            raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * self.load_factor)
        table_ = [elem for elem in self.table if elem]
        self.table = [None] * self.capacity
        self.length = 0

        for elem in table_:
            self[elem[0]] = elem[2]
