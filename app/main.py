from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [None for _ in range(self.capacity)]

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.size = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [None for _ in range(self.capacity)]
        for el in old_hash_table:
            if el:
                self.__setitem__(el[1], el[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.resize()

        hash_key = hash(key)
        hash_index = hash_key % self.capacity

        while True:
            if not self.hash_table[hash_index]:
                self.hash_table[hash_index] = [hash_key, key, value]
                self.size += 1
                break
            if self.hash_table[hash_index][0] == hash_key and \
                    self.hash_table[hash_index][1] == key:
                self.hash_table[hash_index][2] = value
                break
            hash_index = (hash_index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:

        hash_key = hash(key)
        hash_index = hash_key % self.capacity

        while self.hash_table[hash_index]:
            if (self.hash_table[hash_index][0] == hash_key
                    and self.hash_table[hash_index][1] == key):
                return self.hash_table[hash_index][2]
            hash_index = (hash_index + 1) % self.capacity
        raise KeyError(f"{key} key does not exist in falsified dictionary")

    def __len__(self) -> int:
        return self.size
