from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]
        self.storage = 0

    def __setitem__(self,
                    key: (int, float, str, bool, tuple),
                    value: Any) -> None:
        if self.storage == self.threshold:
            self.resize()
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, hashed_key, value]
                self.storage += 1
                break

            if self.hash_table[index][0] == key and \
                    self.hash_table[index][1] == hashed_key:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: (int, float, str, bool, tuple)) -> Any:
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][0] == key and \
                    self.hash_table[index][1] == hashed_key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def resize(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.storage = 0
        old_hash_list = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in old_hash_list:
            if item:
                self.__setitem__(item[0], item[2])

    def __len__(self) -> int:
        return self.storage
