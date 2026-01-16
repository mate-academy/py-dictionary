from copy import deepcopy
from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.length = 0
        self.content = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hashed_result = hash(key)
        threshold = int(self.capacity * self.load_factor)

        if self.length == threshold:
            self.resize()

        index = hashed_result % self.capacity

        while True:
            if not self.content[index]:
                self.content[index] = [key, value, hashed_result]
                self.length += 1
                return
            if key == self.content[index][0] and \
                    hashed_result == self.content[index][2]:
                self.content[index][1] = value
                return
            index = (index + 1) % self.capacity

    def __getitem__(self, item: Hashable) -> list | None:
        hashed_value = hash(item)
        index = hashed_value % self.capacity

        while self.content[index]:
            if self.content[index][0] == item and \
                    self.content[index][2] == hashed_value:
                return self.content[index][1]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        new_bucket = deepcopy(self.content)
        self.length = 0
        self.capacity *= 2
        self.content = [[] for _ in range(self.capacity + 1)]

        for element in new_bucket:
            if element:
                self.__setitem__(element[0], element[1])
