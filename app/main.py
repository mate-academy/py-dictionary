from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self._length = 0
        self._capacity = 8
        self._hashtable: list = [None] * 8

    def __len__(self) -> int:
        return self._length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self._length == int((2 / 3) * self._capacity) + 1:
            self.resize()

        hash_key = hash(key)
        index = hash_key % self._capacity

        if not self._hashtable[index]:
            self._hashtable[index] = (key, value, hash_key)
            self._length += 1
        elif self._hashtable[index][0] == key:
            self._hashtable[index] = (key, value, hash_key)
        else:
            index += 1
            while index <= self._capacity:
                if index == self._capacity:
                    index = 0
                if self._hashtable[index] and self._hashtable[index][0] == key:
                    self._hashtable[index] = (key, value, hash_key)
                    break
                if not self._hashtable[index]:
                    self._hashtable[index] = (key, value, hash_key)
                    self._length += 1
                    break
                index += 1

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self._capacity

        if not self._hashtable[index]:
            raise KeyError()

        if self._hashtable[index][0] != key:
            index += 1
            while index <= self._capacity:
                if index == self._capacity:
                    index = 0
                if self._hashtable[index] and self._hashtable[index][0] == key:
                    return self._hashtable[index][1]
                index += 1
            else:
                raise KeyError()

        return self._hashtable[index][1]

    def resize(self) -> None:
        table = self._hashtable
        self._hashtable = [None] * (self._capacity * 2)
        self._capacity *= 2
        self._length = 0
        [self.__setitem__(table[row][0], table[row][1])
         for row in range(self._capacity // 2) if table[row]]
