from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.bucket_size = 8
        self.bucket: list = [None] * self.bucket_size
        self.load_factor = 2 / 3

    def __setitem__(self, key: Any, value: Any, bucket: list = None) -> None:
        if bucket is None:
            bucket = self.bucket

        hash_value, index = self.get_hash_and_index(key)

        while bucket[index] is not None and key != bucket[index][0]:
            index = (index + 1) % self.bucket_size

        if bucket[index] is None:
            self.length += 1

        bucket[index] = [key, value, hash_value]

        if self.length > self.bucket_size * self.load_factor:
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        hash_value, index = self.get_hash_and_index(key)

        while self.bucket[index] is not None and key != self.bucket[index][0]:
            index = (index + 1) % self.bucket_size
        if self.bucket[index] is None:
            raise KeyError(key)
        return self.bucket[index][1]

    def __len__(self) -> int:
        return self.length

    def get_hash_and_index(self, key: Any) -> tuple:
        hash_value = hash(key)
        index = hash_value % self.bucket_size
        return hash_value, index

    def resize(self) -> None:
        old_bucket = self.bucket
        self.bucket_size *= 2
        self.bucket = [None] * self.bucket_size
        self.length = 0

        for elem in old_bucket:
            if elem is not None:
                key, value, _ = elem
                self.__setitem__(key, value, bucket=self.bucket)
