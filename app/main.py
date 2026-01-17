from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.load_factor = 2 / 3
        self.capacity = 8
        self.threshold = int(self.capacity * self.load_factor)
        self.hash_table = [[] for _ in range(self.capacity)]
        self.size = 0

    def resize(self) -> None:
        hash_table = self.hash_table
        self.capacity *= 2
        self.size = 0
        self.threshold = int(self.capacity * self.load_factor)
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in hash_table:
            if item:
                self.__setitem__(item[0], item[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.resize()

        key_hash = hash(key)
        index = key_hash % self.capacity

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, key_hash, value]
                self.size += 1
                return
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == key_hash):
                self.hash_table[index][2] = value
                return
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.hash_table[index]:
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == key_hash):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.size
