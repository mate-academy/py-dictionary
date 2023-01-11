from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]
        self.current_load = 0
        self.load_factor = 2 / 3

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.current_load > self.capacity * self.load_factor:
            self.resize()
        hash_key = hash(key)
        index = hash_key % self.capacity

        if not self.hash_table[index]:
            self.hash_table[index] = [key, hash_key, value]
            self.current_load += 1
        elif self.hash_table[index][0] == key:
            self.hash_table[index][2] = value
        else:
            index = (index + 1) % self.capacity

            while True:
                if not self.hash_table[index]:
                    self.hash_table[index] = [key, hash_key, value]
                    self.current_load += 1
                    break
                elif self.hash_table[index][0] == key:
                    self.hash_table[index][2] = value
                    break
                index = (index + 1) % self.capacity

    def __getitem__(self, item: Any) -> Any:
        hash_key = hash(item)
        index = hash_key % self.capacity
        while True:
            try:
                for _ in range(self.capacity):
                    if self.hash_table[index][0] == item:
                        return self.hash_table[index][2]
            except IndexError:
                raise KeyError("Missing key")
            break
        for _ in range(self.capacity):
            if self.hash_table[index][0] == item:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def resize(self) -> None:
        self.capacity *= 2
        self.current_load = 0
        old_hash_table = self.hash_table
        self.hash_table = [[] for _ in range(self.capacity)]
        for index in old_hash_table:
            if index:
                self.__setitem__(index[0], index[2])

    def __len__(self) -> int:
        return self.current_load
