from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = self.make_hash_table()

    def make_hash_table(self) -> list:
        return [[] for _ in range(self.capacity)]

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        hash_index = hash_key % self.capacity
        while self.hash_table[hash_index]:
            if (
                    self.hash_table[hash_index][0] == key
                    and self.hash_table[hash_index][1] == hash_key
            ):
                return self.hash_table[hash_index][2]
            hash_index = (hash_index + 1) % self.capacity
        raise KeyError(key)

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.size = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = self.make_hash_table()
        for bucket in old_hash_table:
            if bucket:
                self[bucket[0]] = bucket[2]

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
            if (
                    self.hash_table[hash_index][0] == key
                    and self.hash_table[hash_index][1] == hash_key
            ):
                self.hash_table[hash_index][2] = value
                break

            hash_index = (hash_index + 1) % self.capacity
