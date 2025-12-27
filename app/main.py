from typing import Hashable, Any


class Dictionary:
    CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.threshold = int(self.CAPACITY * self.LOAD_FACTOR)
        self.table = [[] for _ in range(self.CAPACITY)]
        self.length = 0

    def resize_table(self) -> None:
        table_copy = self.table
        self.length = 0
        self.CAPACITY *= 2
        self.threshold = int(self.CAPACITY * self.LOAD_FACTOR)
        self.table = [[] for _ in range(self.CAPACITY)]
        for element in table_copy:
            if element:
                self[element[0]] = element[1]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_ = hash(key)
        index = hash_ % self.CAPACITY

        if self.length == self.threshold:
            self.resize_table()

        while True:
            if not self.table[index]:
                self.table[index] = [key, value, hash_]
                self.length += 1
                return

            if self.table[index][0] == key and \
                    self.table[index][2] == hash_:
                self.table[index][1] = value
                return

            index = (index + 1) % self.CAPACITY

    def __getitem__(self, key: Hashable) -> Any:
        hash_ = hash(key)
        index = hash_ % self.CAPACITY

        while self.table[index]:
            if self.table[index][0] == key and self.table[index][2] == hash_:
                return self.table[index][1]
            index = (index + 1) % self.CAPACITY
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length
