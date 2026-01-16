from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, key: Hashable) -> Any:
        hash_item = hash(key)
        idx = hash_item % self.capacity

        while self.buckets[idx]:
            if (self.buckets[idx][0] == hash_item
                    and self.buckets[idx][1] == key):
                return self.buckets[idx][2]

            idx = (idx + 1) % self.capacity

        raise KeyError(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.resize()

        hash_item = hash(key)
        idx = hash_item % self.capacity

        while True:
            if not self.buckets[idx]:
                self.buckets[idx] = [hash_item, key, value]
                self.size += 1
                break
            if (self.buckets[idx][1] == key
                    and self.buckets[idx][0] == hash_item):
                self.buckets[idx][2] = value
                break

            idx = (idx + 1) % self.capacity

    def resize(self) -> None:
        old_buckets = self.buckets.copy()

        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for item in old_buckets:
            if item:
                self.__setitem__(item[1], item[2])

    def clear(self) -> None:
        self.buckets = [[] for _ in range(self.capacity)]

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        hash_item = hash(key)
        idx = hash_item % self.capacity

        while self.buckets[idx]:
            if (self.buckets[idx][1] == key
                    and self.buckets[idx][0] == hash_item):
                value = self.buckets[idx][2]
                self.buckets[idx] = []
                self.size -= 1
                return value

            idx = (idx + 1) % self.capacity

        if default is not None:
            return default

        raise KeyError(key)
