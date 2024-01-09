from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = int(self.capacity * 2 // 3)
        self.stock = [[] for i in range(self.capacity)]
        self.size = 0

    def resize(self) -> None:
        copy_stock = self.stock
        self.size = 0
        self.capacity *= 2
        self.load_factor = int(self.capacity * 2 // 3)
        self.stock = [[] for i in range(self.capacity)]
        for item in copy_stock:
            if item:
                self.__setitem__(item[0], item[1])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.load_factor:
            self.resize()
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if not self.stock[index]:
                self.stock[index] = [key, value, hash_key]
                self.size += 1
                return
            if self.stock[index][0] == key and\
                    self.stock[index][2] == hash_key:
                self.stock[index][1] = value
                return
            index = (index + 1) % self.capacity

    def __getitem__(self, key: None) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if not self.stock[index]:
                raise KeyError(key)
            if self.stock[index][0] == key and\
                    self.stock[index][2] == hash_key:
                return self.stock[index][1]
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.size
