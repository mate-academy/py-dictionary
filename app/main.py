from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.load_factor = 2 / 3
        self.bucket_size = 8
        self.threshold = int(self.bucket_size * self.load_factor)
        self.hash_table: list = [None] * self.bucket_size

    def resize(self) -> None:
        self.bucket_size *= 2
        self.threshold = int(self.bucket_size * self.load_factor)
        self.length = 0
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.bucket_size
        for element in old_hash_table:
            if element is not None:
                self.__setitem__(element[0], element[1])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self.resize()
        hashed_value = hash(key)
        index = hashed_value % self.bucket_size
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = [key, value, hashed_value]
                self.length += 1
                break
            elif key == self.hash_table[index][0]:
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.bucket_size

    def __getitem__(self, input_key: Hashable) -> None:
        hashed_value = hash(input_key)
        index = hashed_value % self.bucket_size
        while self.hash_table[index] is not None:
            key, value, hashed_value = self.hash_table[index]
            if key == input_key:
                return value
            index = (index + 1) % self.bucket_size
        raise KeyError

    def __len__(self) -> int:
        return self.length
