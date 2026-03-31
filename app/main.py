from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.hash_table = [[] for _ in range(self.capacity)]
        self.threshold = int(self.capacity * 2 / 3)

    def resize(self) -> None:
        prev_hash_table = self.hash_table
        self.capacity *= 2
        self.size = 0
        self.hash_table = [[] for _ in range(self.capacity)]
        self.threshold = int(self.capacity * 2 / 3)
        for item in prev_hash_table:
            if item:
                self[item[0]] = item[1]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size >= self.threshold:
            self.resize()

        hash_key = hash(key)
        hash_index = hash_key % self.capacity

        while True:
            if not self.hash_table[hash_index]:
                self.hash_table[hash_index] = [key, value, hash_key]
                self.size += 1
                break

            if self.hash_table[hash_index][0] == key:
                self.hash_table[hash_index][1] = value
                break

            hash_index = (hash_index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> None:
        hash_key = hash(key)
        hash_index = hash_key % self.capacity

        while self.hash_table[hash_index]:
            if (self.hash_table[hash_index][2] == hash_key
                    and self.hash_table[hash_index][0] == key):
                return self.hash_table[hash_index][1]
            hash_index = (hash_index + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> None:
        return self.size
