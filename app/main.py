from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = 0.66
        self.size = 0
        self.hash_table = [None] * 8

    def __getitem__(self, key: Hashable) -> Any:
        index = self.__index_from_key(key)

        while self.hash_table[index]:
            if self.__item_key(self.hash_table[index]) == key:
                return self.__item_value(self.hash_table[index])
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size > self.capacity * self.threshold:
            self.__resize()

        index = self.__index_from_key(key)

        while True:
            item = self.hash_table[index]

            if not self.hash_table[index] or self.__item_key(item) == key:
                if not self.hash_table[index]:
                    self.size += 1
                self.hash_table[index] = (key, hash(key), value)
                break
            index = (index + 1) % self.capacity

    def __resize(self) -> None:
        self.capacity *= 2
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.size = 0

        for item in old_hash_table:
            if item:
                self.__setitem__(
                    self.__item_key(item),
                    self.__item_value(item)
                )

    def __len__(self) -> int:
        return self.size

    def __index_from_key(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __index_from_hash(self, hash_: int) -> int:
        return hash_ % self.capacity

    @staticmethod
    def __item_hash(item: Any) -> Any:
        return item[1]

    @staticmethod
    def __item_value(item: Any) -> Any:
        return item[2]

    @staticmethod
    def __item_key(item: Any) -> Any:
        return item[0]
