from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.length = 0
        self.hash_table = [None for _ in range(self.size)]

    def resize(self) -> None:
        if not len(self) > (self.size * (2 / 3)):
            return
        self.length = 0
        temp = self.hash_table
        self.size *= 2
        self.hash_table = [None for _ in range(self.size)]
        for el in temp:
            if el is not None:
                self[el[0]] = el[2]

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_ = hash(key)
        index_ = hash_ % self.size
        while self.hash_table[index_]:
            if self.hash_table[index_] and self.hash_table[index_][0] == key:
                self.hash_table[index_] = [key, hash_, value]
                return
            index_ = (index_ + 1) % self.size
        self.hash_table[index_] = [key, hash_, value]
        self.length += 1
        self.resize()

    def __getitem__(self, key: Hashable) -> None:
        index_ = hash(key) % self.size
        for _ in range(self.size):
            if self.hash_table[index_] and self.hash_table[index_][0] == key:
                return self.hash_table[index_][2]
            index_ = (index_ + 1) % self.size
        raise KeyError(f"{key}")
