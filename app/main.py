from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity_table = 8
        self.threshold_table = int(self.capacity_table * (2 / 3))
        self.size_table = 0
        self.hash_table = [[] for _ in range(self.capacity_table)]

    def __len__(self) -> int:
        return self.size_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size_table == self.threshold_table:
            self.resize_table()
        key_hash = hash(key)
        self.fill_table(key, value, key_hash)

    def __getitem__(self, key: Hashable) -> list | None:
        key_hash = hash(key)
        hash_index = key_hash % self.capacity_table
        while self.hash_table[hash_index]:
            if (self.hash_table[hash_index][2] == key_hash
                    and self.hash_table[hash_index][0] == key):
                return self.hash_table[hash_index][1]
            hash_index = (hash_index + 1) % self.capacity_table
        raise KeyError(f"{key} does not exist")

    def resize_table(self) -> None:
        self.capacity_table *= 2
        self.threshold_table = int(self.capacity_table * (2 / 3))
        self.size_table = 0
        prev_table = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity_table)]
        for item in prev_table:
            if item:
                self[item[0]] = item[1]

    def fill_table(self, key: Hashable, value: Any, hash_key: int) -> None:
        hash_index = hash_key % self.capacity_table

        while True:
            if not self.hash_table[hash_index]:
                self.size_table += 1
                self.hash_table[hash_index] = [key, value, hash_key]
                break
            if (self.hash_table[hash_index][2] == hash_key
                    and self.hash_table[hash_index][0] == key):
                self.hash_table[hash_index][1] = value
                break
            hash_index = (hash_index + 1) % self.capacity_table
