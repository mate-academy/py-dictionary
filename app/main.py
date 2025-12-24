from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.table = [[] for _ in range(self.capacity)]
        self.length = 0
        self.threshold = int(self.capacity * self.load_factor)

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity

        while self.table[index]:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity

        raise KeyError

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self.resize()
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if not self.table[index]:
                self.table[index] = [key, value, hash_key]
                self.length += 1
                break
            if key == self.table[index][0]:
                self.table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        new_table = self.table
        self.length = 0
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.threshold = int(self.capacity * self.load_factor)
        for element in new_table:
            if element:
                self.__setitem__(element[0], element[1])
