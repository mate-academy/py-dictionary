from typing import Any
from typing import Hashable


class Dictionary:

    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * initial_capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= (2 / 3) * self.capacity:
            self.resize_table()
        index = hash(key) % self.capacity
        if self.table[index] is None:
            self.table[index] = []
        for step, pair in enumerate(self.table[index]):
            if pair[0] == key:
                self.table[index][step] = (key, value)
                break
        else:
            self.table[index].append((key, value))
            self.size += 1

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        if self.table[index] is not None:
            for i in self.table[index]:
                if i[0] == key:
                    return i[1]
        raise KeyError

    def __len__(self) -> int:
        return self.size

    def resize_table(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity
        for bucket in self.table:
            if bucket is not None:
                for key, value in bucket:
                    index = hash(key) % new_capacity
                    if new_table[index] is None:
                        new_table[index] = []
                    new_table[index].append((key, value))
        self.table = new_table
        self.capacity = new_capacity
