from typing import Any


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.table = [[]] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length > self.capacity * self.LOAD_FACTOR:
            self.__resize()
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            if not self.table[index]:
                self.table[index] = [key, key_hash, value]
                self.length += 1
                break
            if (
                self.table[index][0] == key
                and self.table[index][1] == key_hash
            ):
                self.table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, item: Any) -> Any:
        index = hash(item) % self.capacity

        while self.table[index]:
            if self.table[index][0] == item:
                return self.table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def __resize(self) -> None:
        self.capacity *= 2
        self.length = 0
        old_table = self.table
        self.table = [[]] * self.capacity
        for data in old_table:
            if data:
                key, _, value = data
                self.__setitem__(key, value)

    def __len__(self) -> int:
        return self.length
