from typing import Any, Hashable


class Dictionary:
    bucket_size = 8

    def __init__(self) -> None:
        self.buckets = [[] for bucket in range(self.bucket_size)]

    def resize_bucket(self) -> None:
        busy_bucket = [value for value in self.buckets if value != []]
        self.bucket_size += self.bucket_size
        self.__init__()
        for key in busy_bucket:
            self.__setitem__(key[0], key[1])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        keys = [key[0] for key in self.buckets if key]
        if key in keys:
            old_value = (key, self[key])
            index = self.buckets.index(old_value)
            self.buckets[index] = (key, value)
            return

        hashed_value = hash(key)

        index = hashed_value % self.bucket_size
        while self.buckets[index]:
            index = (index + 1) % self.bucket_size

        self.buckets[index] = (key, value)
        if self.__len__() > self.bucket_size * 2 / 3:
            self.resize_bucket()

    def __getitem__(self, key: Hashable) -> Any:
        for bucket in self.buckets:
            if bucket and bucket[0] == key:
                return bucket[1]
        raise KeyError

    def __len__(self) -> int:
        return len([i for i in self.buckets if i != []])
