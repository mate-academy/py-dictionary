from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = int(self.capacity * 2 / 3)
        self.hash_table = [[]] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, key: Any) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][1] == hash_key and \
                    self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError(f"'{key}'")

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length > self.load_factor:
            self.resize()
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, hash_key, value]
                self.length += 1
                break
            if self.hash_table[index][1] == hash_key and \
                    self.hash_table[index][0] == key:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        self.length = 0
        self.capacity *= 2
        self.load_factor = int(self.capacity * 2 / 3)
        old_hash_table = self.hash_table
        self.hash_table = [[]] * self.capacity
        for table in old_hash_table:
            if table:
                self.__setitem__(table[0], table[2])
