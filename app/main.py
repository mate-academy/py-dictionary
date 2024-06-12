from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = self.create_hash_table()

    def create_hash_table(self) -> list:
        return [[] for _ in range(self.capacity)]

    def resize_capacity(self) -> None:
        this_hash_table = self.hash_table
        self.capacity *= 2
        self.hash_table = self.create_hash_table()
        self.length = 0
        self.threshold = int(self.capacity * 2 / 3)

        for item in this_hash_table:
            if len(item) > 0:
                self.__setitem__(item[0], item[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.threshold == self.length:
            self.resize_capacity()

        hash_value = hash(key)
        hash_index = hash_value % self.capacity

        while True:
            if not self.hash_table[hash_index]:
                self.hash_table[hash_index] = [key, hash_value, value]
                self.length += 1
                break
            if (self.hash_table[hash_index][1] == hash_value
                    and self.hash_table[hash_index][0] == key):
                self.hash_table[hash_index][2] = value
                break

            hash_index = (hash_index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:

        hash_value = hash(key)
        hash_index = hash_value % self.capacity

        while self.hash_table[hash_index]:
            if (self.hash_table[hash_index][1] == hash_value
                    and self.hash_table[hash_index][0] == key):
                return self.hash_table[hash_index][2]
            hash_index = (hash_index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length
