from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.bucket_capacity = 8
        self.load_factor = 2 / 3
        self.bucket = [[] for _ in range(self.bucket_capacity)]
        self.current_size = 0
        self.threshold = int(self.bucket_capacity * self.load_factor)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.current_size == self.threshold:
            self.resize()
        content = [key, hash(key), value]
        cell_number = hash(key) % self.bucket_capacity
        while True:
            if not self.bucket[cell_number]:
                self.bucket[cell_number] = content
                self.current_size += 1
                return

            if (self.bucket[cell_number][0] == key
                    and hash(key) == self.bucket[cell_number][1]):
                self.bucket[cell_number][2] = value
                break

            cell_number = (cell_number + 1) % self.bucket_capacity

    def __getitem__(self, item: Hashable) -> list[Hashable]:
        cell_number = hash(item)
        index = cell_number % self.bucket_capacity
        if self.current_size:
            while True:
                if (self.bucket[index][0] == item
                        and self.bucket[index][1] == hash(item)):
                    return self.bucket[index][2]
                index = (index + 1) % self.bucket_capacity
        raise KeyError(item)

    def __len__(self) -> int:
        return self.current_size

    def resize(self) -> None:
        old_one = self.bucket.copy()
        self.bucket_capacity *= 2
        self.threshold = int(self.bucket_capacity * 2 / 3)
        self.current_size = 0
        self.bucket = [[] for _ in range(self.bucket_capacity)]

        for item in old_one:
            if item:
                self.__setitem__(item[0], item[2])
