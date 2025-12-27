from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [None for _ in range(self.capacity)]

    def resize(self) -> None:
        self.capacity *= 2
        self.size = 0
        self.threshold = int(self.capacity * 2 / 3)
        temporary_table = self.hash_table.copy()
        self.hash_table = [None for _ in range(self.capacity)]

        for element in temporary_table:
            if element:
                self.__setitem__(element[0], element[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.size == self.threshold:
            self.resize()

        hash_value = hash(key)
        index = hash_value % self.capacity

        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, hash_value, value]
                self.size += 1
                break

            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_value):
                self.hash_table[index][2] = value
                break

            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any | KeyError:
        hash_value = hash(key)
        index = hash_value % self.capacity

        while self.hash_table[index]:
            if (self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_value):
                return self.hash_table[index][2]

            index = (index + 1) % self.capacity

        raise KeyError

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        self.hash_table = [None for _ in range(self.capacity)]
        self.size = 0
