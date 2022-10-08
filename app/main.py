from typing import Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.fullness = 0
        self.buckets = [None] * self.capacity

    def __resizer(self) -> None:
        self.capacity *= 2
        self.fullness, old_buckets = 0, self.buckets
        self.buckets = [None] * self.capacity

        for item in old_buckets:
            if item:
                self.__setitem__(item[0], item[1])

    def __setitem__(self, key: Hashable, value: any) -> None:
        if self.fullness >= (self.capacity * self.load_factor):
            self.__resizer()

        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while True:
            if self.buckets[index] is None:
                self.buckets[index] = [key, value, hashed_key]
                self.fullness += 1
                break
            if self.buckets[index][0] == key and \
                    self.buckets[index][2] == hashed_key:
                self.buckets[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> any:
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while self.buckets[index]:
            if self.buckets[index][2] == hashed_key and \
                    self.buckets[index][0] == key:
                return self.buckets[index][1]
            index = (index + 1) % self.capacity
        raise KeyError()

    def __len__(self) -> int:
        return self.fullness
