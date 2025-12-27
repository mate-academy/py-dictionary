from typing import Hashable, Any


class Dictionary:

    def __init__(self) -> None:
        self._capacity = 8
        self._threshold = int(self._capacity * 2 / 3)
        self._length = 0
        self.table = [[] for _ in range(self._capacity)]

    def __len__(self) -> int:
        return self._length

    def __resize_table(self) -> None:

        table = self.table
        self._length = 0
        self._capacity *= 2
        self._threshold = int(self._capacity * 2 / 3)
        self.table = [[] for _ in range(self._capacity)]

        for cell in table:
            if cell:
                self[cell[0]] = cell[1]

    def __getitem__(self, item: Hashable) -> list or None:
        hash_ = hash(item)
        index = hash_ % self._capacity

        while self.table[index]:

            if self.table[index][0] == item and hash_ == self.table[index][2]:
                return self.table[index][1]
            index = (index + 1) % self._capacity

        raise KeyError(item)

    def __setitem__(self, key: Hashable, value: Any) -> None:

        if len(self) == self._threshold:
            self.__resize_table()

        hash_ = hash(key)
        index = hash_ % self._capacity

        while True:
            if not self.table[index]:
                self.table[index] = [key, value, hash_]
                self._length += 1
                break
            if key == self.table[index][0] and hash_ == self.table[index][2]:
                self.table[index][1] = value
                break
            index = (index + 1) % self._capacity

    def clear(self) -> None:
        self._capacity = 8
        self._length = 0
        self.table = [[] for _ in range(self._capacity)]
