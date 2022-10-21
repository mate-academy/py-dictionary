from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_list = [[] for _ in range(self.capacity)]

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length == self.threshold:
            self.resize()
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        while True:
            if not self.hash_list[index_]:
                self.hash_list[index_] = [key, hash_, value]
                self.length += 1
                break
            if self.hash_list[index_][0] == key and\
                    self.hash_list[index_][1] == hash_:
                self.hash_list[index_][2] = value
                break
            index_ = (index_ + 1) % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.length = 0
        old_list = self.hash_list
        self.hash_list = [[] for _ in range(self.capacity)]
        for item in old_list:
            if item:
                self.__setitem__(item[0], item[2])

    def __getitem__(self, key: Any) -> list:
        hash_ = hash(key)
        index_ = hash_ % self.capacity
        while self.hash_list[index_]:
            if self.hash_list[index_][1] == hash_ \
                    and self.hash_list[index_][0] == key:
                return self.hash_list[index_][2]
            index_ = (index_ + 1) % self.capacity
        raise KeyError(key)
