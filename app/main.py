from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(2 / 3 * self.capacity)
        self.size = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def resize(self) -> None:
        self.capacity *= 2
        self.size = 0
        self.threshold = int(2 / 3 * self.capacity)
        old_hash_table = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity)]
        for pair in old_hash_table:
            if pair:
                self.__setitem__(pair[0], pair[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.resize()

        hash_key = hash(key)
        hash_index = hash_key % self.capacity
        while True:
            if not self.hash_table[hash_index]:
                self.hash_table[hash_index] = [key, hash_key, value]
                self.size += 1
                break
            if self.hash_table[hash_index][0] == key:
                self.hash_table[hash_index][2] = value
                break

            hash_index = (hash_index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        hash_index = hash_key % self.capacity
        while self.hash_table[hash_index]:
            if self.hash_table[hash_index][0] == key:
                return self.hash_table[hash_index][2]
            hash_index = (hash_index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
