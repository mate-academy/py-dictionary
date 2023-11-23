from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.storage = [[] for _ in range(self.capacity)]
        self.size = 0

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.resize()
        hash_key = hash(key) % self.capacity
        while True:
            if self.storage[hash_key] != []:
                hash_key += 1
                if hash_key > self.capacity - 1:
                    hash_key = 0
            else:
                self.storage[hash_key] = [key, value, hash(key)]
                self.size += 1
                break

    def resize(self) -> None:
        if self.size > 2 / 3 * self.capacity:
            self.capacity *= 2
            old_elements = self.storage
            self.storage = [[] for _ in range(self.capacity)]
            self.size = 0
            for element in old_elements:
                if element != []:
                    self.__setitem__(element[2], element[1])

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key) % self.capacity
        if not self.storage[hash_key]:
            raise KeyError
        else:
            return self.storage[hash_key][1]

    def __len__(self) -> int:
        return self.size
