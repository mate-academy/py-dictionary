from typing import Hashable, Any


class Dictionary:

    def __init__(self) -> None:
        self.load_factor = 2 / 3
        self.capacity = 8
        self.length = 0
        self.threshold = int(self.capacity * self.load_factor)
        self.hash_table = self.create_hash_table()

    def resize(self) -> None:
        hash_table = self.hash_table
        self.length = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * self.load_factor)
        self.hash_table = self.create_hash_table()

        for element in hash_table:
            if element:
                self.__setitem__(element[0], element[2])

    def create_hash_table(self) -> list:
        return [[] for _ in range(self.capacity)]

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity

        while self.hash_table[index]:
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_key):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if self.length == self.threshold:
            self.resize()

        key_hash = (hash(key))
        hash_index = key_hash % self.capacity

        while True:
            if not self.hash_table[hash_index]:
                self.hash_table[hash_index] = [key, key_hash, value]
                self.length += 1
                break
            if (self.hash_table[hash_index][0] == key
                    and self.hash_table[hash_index][1] == key_hash):
                self.hash_table[hash_index][2] = value
                break
            hash_index = (hash_index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length
