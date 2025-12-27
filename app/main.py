import math

from typing import Any


class Dictionary:

    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hashtable = self.create_hashtable()
        self.threshold = self.create_threshold()

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length == self.threshold:
            self.resize_hashtable()
        hash_key = hash(key)
        index = self.find_index(key)

        while True:
            if not self.hashtable[index]:
                self.hashtable[index] = [key, value, hash_key]
                self.length += 1
                return

            if key == self.hashtable[index][0] and \
                    hash_key == self.hashtable[index][2]:
                self.hashtable[index][1] = value
                return

            index = (index + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        index = self.find_index(key)
        hash_key = hash(key)
        while True:
            if not self.hashtable[index]:
                raise KeyError(key)
            if self.hashtable[index][0] == key and \
                    self.hashtable[index][2] == hash_key:
                return self.hashtable[index][1]
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def find_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def resize_hashtable(self) -> None:
        copied_hashtable = self.hashtable
        self.length = 0
        self.capacity *= 2
        self.threshold = self.create_threshold()
        self.hashtable = self.create_hashtable()

        for item in copied_hashtable:
            if item:
                self.__setitem__(item[0], item[1])

    def create_hashtable(self) -> list:
        return [None for _ in range(self.capacity)]

    def create_threshold(self) -> int:
        return math.floor(self.capacity * 2 / 3)
