from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.threshold = self.size * 2 // 3
        self.bucket = [[] for _ in range(self.size)]

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if self.__len__() >= self.threshold:
            self.resize_bucket()

        key_hash = hash(key)
        index = key_hash % self.size
        while True:
            if not self.bucket[index] or self.bucket[index][0] == key:
                self.bucket[index] = [key, key_hash, value]
                break
            index = (index + 1) % self.size

    def __len__(self) -> int:
        return len(self.bucket) - self.bucket.count([])

    def resize_bucket(self) -> None:
        self.size *= 2
        self.threshold = self.size * 2 // 3
        old_bucket = self.bucket
        self.bucket = [[] for _ in range(self.size)]
        for item in old_bucket:
            if item:
                self.__setitem__(item[0], item[-1])

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self.size
        while self.bucket[index]:
            if self.bucket[index][0] == key:
                return self.bucket[index][-1]
            index = (index + 1) % self.size
        raise KeyError(key)
