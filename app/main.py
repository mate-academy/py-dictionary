from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshhold = int(self.capacity * 2 / 3)
        self.length = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshhold:
            self.resize()
        key_hash = hash(key)
        index = key_hash % self.capacity

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, value, key_hash]
                self.length += 1
                break
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][2] == key_hash):
                self.hash_table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity
        cell = self.hash_table[index]
        while cell:
            if cell[0] == key and cell[2] == key_hash:
                return cell[1]
            index = (index + 1) % self.capacity
            cell = self.hash_table[index]
        raise KeyError(key)

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        old_table = self.hash_table.copy()
        self.length = 0
        self.capacity *= 2
        self.threshhold = int(self.capacity * 2 / 3)
        self.hash_table = [[] for _ in range(self.capacity)]
        for element in old_table:
            if element:
                self[element[0]] = element[1]

    def clear(self) -> None:
        self.capacity = 8
        self.threshhold = int(self.capacity * 2 / 3)
        self.length = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError(key):
            return default
