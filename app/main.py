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
            self.recise()
        hash_data = hash(key)
        index_data = hash_data % self.capacity
        while True:
            if not self.hash_list[index_data]:
                self.hash_list[index_data] = [key, hash_data, value]
                self.length += 1
                break
            if self.hash_list[index_data][0] == key and\
                    self.hash_list[index_data][1] == hash_data:
                self.hash_list[index_data][2] = value
                break
            index_data = (index_data + 1) % self.capacity

    def recise(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.length = 0
        old_data = self.hash_list
        self.hash_list = [[] for _ in range(self.capacity)]
        for item in old_data:
            if item:
                self.__setitem__(item[0], item[2])

    def __getitem__(self, key: Any) -> list:
        hash_data = hash(key)
        index_data = hash_data % self.capacity
        while self.hash_list[index_data]:
            if self.hash_list[index_data][1] == hash_data \
                    and self.hash_list[index_data][0] == key:
                return self.hash_list[index_data][2]
            index_data = (index_data + 1) % self.capacity
        raise KeyError(key)
