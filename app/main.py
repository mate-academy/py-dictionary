from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.threshold = int(self.capacity * self.load_factor)
        self.length = 0
        self.hash_table = self.make_hash_table()

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self.resize()

        hash_key = hash(key)
        hash_index = hash_key % self.capacity

        while True:
            if not self.hash_table[hash_index]:
                self.hash_table[hash_index] = [key, hash_key, value]
                self.length += 1
                break
            if (
                    self.hash_table[hash_index][0] == key
                    and self.hash_table[hash_index][1] == hash_key
            ):
                self.hash_table[hash_index][2] = value
                break
            hash_index = (hash_index + 1) % self.capacity

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

    def make_hash_table(self) -> list[list]:
        return [[] for _ in range(self.capacity)]

    def resize(self) -> None:
        previous_hash_table = self.hash_table
        self.length = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * self.load_factor)
        self.hash_table = self.make_hash_table()

        for item in previous_hash_table:
            if item:
                self.__setitem__(item[0], item[2])
