from typing import Hashable, Any


class Dictionary:

    THRESHOLD = 2 / 3

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.threshold = int(self.capacity * self.THRESHOLD)
        self.hash_table = [None for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.resize()
        hash_ = hash(key)
        index = hash_ % self.capacity
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = (key, hash_, value)
                self.size += 1
                return
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, hash_, value)
                return
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        hash_ = hash(key)
        index = hash_ % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        self.capacity *= 2
        self.size = 0
        self.threshold = int(self.capacity * self.THRESHOLD)
        old_table = self.hash_table
        self.hash_table = [None for _ in range(self.capacity)]
        for tuple_ in old_table:
            if tuple_ is not None:
                self.__setitem__(tuple_[0], tuple_[2])
