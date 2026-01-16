from __future__ import annotations


class Dictionary:
    def __init__(self) -> None:
        self.length = 8
        self.used_hash = 0
        self.hash_table: list = [None] * self.length

    def resize_hash(self) -> None:
        old_hash = self.hash_table
        self.length *= 2
        self.hash_table = [None] * self.length
        for element in old_hash:
            if element:
                hash_key = hash(element[0])
                index = hash_key % self.length
                while self.hash_table[index]:
                    hash_key += 1
                    index = hash_key % self.length
                self.hash_table[index] = (element[0], element[1], element[2])

    def __setitem__(self, key: any, value: any) -> None:
        if isinstance(key, (list, dict, set)):
            raise TypeError(f"unhashable type: {type(key)}")

        hash_key = hash(key)
        index = hash_key % self.length
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = (key, hash(key), value)
                return
            hash_key += 1
            index = hash_key % self.length
        self.hash_table[index] = (key, hash(key), value)
        self.used_hash += 1

        if self.used_hash > self.length * (2 / 3):
            self.resize_hash()

    def __getitem__(self, key: any) -> any:
        hash_key = hash(key)
        index = hash_key % self.length
        if not self.hash_table[index]:
            raise KeyError
        while self.hash_table[index][0] != key:
            hash_key += 1
            index = hash_key % self.length
        return self.hash_table[index][2]

    def __len__(self) -> int:
        return self.used_hash
