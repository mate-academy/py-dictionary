from typing import Any, Hashable


class Dictionary:

    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.buckets = self.create_buckets()
        self.threshold = self.create_threshold()

    def create_buckets(self) -> list:
        return [[] for _ in range(self.capacity)]

    def create_threshold(self) -> int:
        return int(self.capacity * 2 / 3)

    def create_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.resize()
        hash_key = hash(key)
        index = self.create_index(key)

        while True:
            if not self.buckets[index]:
                self.buckets[index] = [key, value, hash_key]
                self.size += 1
                break

            if self.buckets[index][2] == hash_key and \
                    self.buckets[index][0] == key:
                self.buckets[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        index = self.create_index(key)
        hash_key = hash(key)

        while True:
            if not self.buckets[index]:
                raise KeyError
            if self.buckets[index][2] == hash_key and \
                    self.buckets[index][0] == key:
                return self.buckets[index][1]
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        old_hash = self.buckets
        self.size = 0
        self.capacity *= 2
        self.buckets = self.create_buckets()
        self.threshold = self.create_threshold()

        for item in old_hash:
            if item:
                self.__setitem__(item[0], item[1])

    def __len__(self) -> int:
        return self.size
