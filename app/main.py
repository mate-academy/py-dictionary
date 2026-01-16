from typing import Hashable, Any


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.buckets = [[] for _ in range(self.capacity)]
        self.length = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self.resize_buckets()
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while True:

            if not self.buckets[index]:
                self.buckets[index] = [key, value, hashed_key]
                self.length += 1
                return
            if key == self.buckets[index][0] and \
                    hashed_key == self.buckets[index][2]:
                self.buckets[index][1] = value
                return
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity

        while True:
            if not self.buckets[index]:
                raise KeyError(key)
            if self.buckets[index][0] == key and \
                    self.buckets[index][2] == hash_key:
                return self.buckets[index][1]
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def resize_buckets(self) -> None:
        copy_of_buckets = self.buckets
        self.length = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.buckets = [[] for _ in range(self.capacity)]
        for item in copy_of_buckets:
            if item:
                self.__setitem__(item[0], item[1])
