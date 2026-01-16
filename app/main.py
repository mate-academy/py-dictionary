from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.table = [None for _ in range(self.size)]

    def __len__(self) -> int:
        count = 0
        for i in self.table:
            if i:
                count += 1
        return count

    def __getitem__(self, key: Any) -> Any:
        index_by_hash = hash(key) % self.size
        while True:
            if self.table[index_by_hash] is None:
                raise KeyError
            elif (self.table[index_by_hash][0] == key
                  and self.table[index_by_hash][1] == hash(key)):
                return self.table[index_by_hash][2]
            else:
                index_by_hash = (index_by_hash + 1) % self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.__len__() >= self.size * 0.6:
            self.size *= 2
            new_table = [None for _ in range(self.size)]
            for i in self.table:
                if i is not None:
                    old_key, old_hash, old_value = i
                    index_by_hash = old_hash % self.size
                    while new_table[index_by_hash] is not None:
                        index_by_hash = (index_by_hash + 1) % self.size
                    new_table[index_by_hash] = [old_key, old_hash, old_value]
            self.table = new_table

        index_by_hash = hash(key) % self.size
        hash_key = hash(key)
        while self.table[index_by_hash] is not None:
            if (
                    self.table[index_by_hash][0] == key
                    and self.table[index_by_hash][1] == hash_key
            ):
                self.table[index_by_hash][2] = value
                return
            index_by_hash = (index_by_hash + 1) % self.size
        self.table[index_by_hash] = [key, hash_key, value]
