from typing import Hashable, Any


class Dictionary:
    TABLE_CAPACITY = 8
    LOAD_FACTOR = 2 / 3

    def __init__(self, capacity: int = TABLE_CAPACITY) -> None:
        self.capacity = capacity
        self.size = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def hash_table_index(self, key: Hashable) -> int:
        hashed_key = hash(key)
        index = hashed_key % self.capacity

        return index

    def resize_table(self) -> None:
        threshold = self.capacity * self.LOAD_FACTOR

        if self.size > threshold:
            self.capacity *= 2
            old_hash_table = self.hash_table

            self.hash_table = [[] for _ in range(self.capacity)]
            self.size = 0

            for item in old_hash_table:
                if item:
                    key, hash_, value = item
                    self.__setitem__(key, value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.hash_table_index(key)

        while self.hash_table[index]:
            key_, hash_, value_ = self.hash_table[index]
            if key == key_:
                self.hash_table[index] = (key, hash(key), value)
                return
            index = (index + 1) % self.capacity

        self.size += 1
        self.hash_table[index] = (key, hash(key), value)
        self.resize_table()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.hash_table_index(key)

        while self.hash_table[index]:
            key_, hash_, value = self.hash_table[index]
            if key == key_:
                return value
            index = (index + 1) % self.capacity

        raise KeyError

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self.capacity)]
        self.size = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:
        return self.size
