from typing import Hashable, Any
from copy import deepcopy


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.load_factor = 0.66
        self.data = [[] for _ in range(self.capacity)]

    def resize(self) -> None:
        new_copy = deepcopy(self.data)
        self.length = 0
        self.capacity *= 2
        self.data = [[] for _ in range(self.capacity + 1)]
        for item in new_copy:
            if item:
                self.__setitem__(item[0], item[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hashed = hash(key)
        index = hashed % self.capacity
        while True:
            if not self.data[index]:
                self.data[index] = [key, hashed, value]
                self.length += 1
                break
            if key == self.data[index][0]:
                self.data[index][2] = value
                break
            index = (index + 1) % self.capacity
        threshold = int(self.capacity * self.load_factor)
        if self.length == threshold:
            self.resize()

    def __getitem__(self, key: Any) -> object:
        hashed = hash(key)
        index = hashed % self.capacity
        while self.data[index]:
            if self.data[index][0] == key:
                return self.data[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def get(self, key: Hashable, default: None = None) -> any:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self.data = [[]] * self.capacity
        self.length = 0
