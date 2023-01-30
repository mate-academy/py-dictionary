from typing import Hashable, Any


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]
        self.threshold = int(self.capacity * self.LOAD_FACTOR)
        self.size = 0

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity

        while self.hash_table[index]:
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_key):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity

        raise KeyError

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self._resize()
        hash_key = hash(key)
        index = hash_key % self.capacity

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, hash_key, value]
                self.size += 1
                break

            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_key):
                self.hash_table[index][2] = value
                break

            index = (index + 1) % self.capacity

    def _resize(self) -> None:
        new_hash_table = self.hash_table
        self.size = 0
        self.capacity *= 2
        self.hash_table = [[] for _ in range(self.capacity)]
        self.threshold = int(self.capacity * self.LOAD_FACTOR)

        for elements in new_hash_table:
            if elements:
                self.__setitem__(elements[0], elements[2])

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self.capacity)]
        self.threshold = int(self.capacity * self.LOAD_FACTOR)
        self.size = 0
        self.capacity = 8
