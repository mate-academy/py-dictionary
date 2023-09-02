from typing import Any


class Dictionary:
    pass

    def __init__(self) -> None:
        self.size = 0
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]

    def resize(self) -> None:
        old_hash_table = self.hash_table
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.size = 0
        self.hash_table = [[] for _ in range(self.capacity)]
        for cell in old_hash_table:
            if cell:
                self.__setitem__(cell[0], cell[1])

    def __setitem__(self, key: int, value: Any) -> None:
        if self.size == self.threshold:
            self.resize()
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, value, key_hash]
                self.size += 1
                break

            if self.hash_table[index][0] == key:
                self.hash_table[index][1] = value
                break

            index = (index + 1) % self.capacity

    def __getitem__(self, key: int) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][2] == key_hash \
                    and self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
