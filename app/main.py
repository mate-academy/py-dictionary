from typing import Any


class Dictionary:

    def __init__(self, buckets: int = 8, length: int = 0) -> None:
        self.size = buckets
        self.buckets = [[] for _ in range(self.size)]
        self.threshold = int(self.size * 2 / 3)
        self.length = length

    def __repr__(self) -> str:
        return "\n".join([f"{self.__class__.__name__}"
                          f"(key, value, hashed_key) {bucket}"
                          for bucket in self.buckets])

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = hash_key % self.size

        while True:
            if not self.buckets[index]:
                raise KeyError(f"There is no such a key '{key}'")
            if self.buckets[index][0] == key and\
                    self.buckets[index][2] == hash_key:
                return self.buckets[index][1]
            index = (index + 1) % self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length == self.threshold:
            buckets_copy = self.buckets
            self.size *= 2
            self.length = 0
            self.threshold = int(self.size * 2 / 3)
            self.buckets = [[] for _ in range(self.size)]
            for bucket in buckets_copy:
                if bucket:
                    self.__setitem__(bucket[0], bucket[1])
        hashed_key = hash(key)
        index = hashed_key % self.size

        while True:
            if not self.buckets[index]:
                self.buckets[index] = [key, value, hashed_key]
                self.length += 1
                return
            if key == self.buckets[index][0] and \
                    hashed_key == self.buckets[index][2]:
                self.buckets[index][1] = value
                return
            index = (index + 1) % self.size

    def __len__(self) -> int:
        return self.length
