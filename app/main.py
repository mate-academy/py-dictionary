from typing import Any


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.DELETED = object()
        self.capacity = capacity
        self.length = 0
        self.table: list[list[Any]] = \
            [[None, None, None] for _ in range(self.capacity)]
        self.threshold = 2 / 3

    @staticmethod
    def get_index(key: Any, capacity: int) -> int:
        return hash(key) % capacity

    def find_key(self, index: int, key: Any) -> int:
        while self.table[index][0] != key:
            if self.table[index][0] is None:
                raise KeyError
            index += 1
            index %= self.capacity
        return index

    def __clear_table__(self) -> None:
        self.table = [[None, None, None] for _ in range(self.capacity)]
        self.length = 0

    def clear(self) -> None:
        self.__clear_table__()

    def __extend_table__(self) -> None:
        temptable = []
        for key, value, hash_val in self.table:
            if key is not None and key != self.DELETED:
                temptable.append([key, value, hash_val])
        self.capacity *= 2
        self.__clear_table__()
        for key, value, hash_val in temptable:
            self.__setitem__(key, value)

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, key: Any) -> Any:
        index = self.get_index(key, self.capacity)
        index = self.find_key(index, key)
        return self.table[index][1]

    def __setitem__(self, key: Any, value: Any) -> None:
        if key is None:
            raise KeyError
        index = self.get_index(key, self.capacity)
        while (self.table[index][0] is not None
               and self.table[index][0] != self.DELETED):
            if self.table[index][0] == key:
                self.length -= 1
                break
            index += 1
            if index == self.capacity:
                index = 0

        self.table[index][2] = hash(key)
        self.table[index][1] = value
        self.table[index][0] = key
        self.length += 1
        if self.length >= self.capacity * self.threshold:
            self.__extend_table__()

    def get(self, key: Any, return_is_none: Any = None) -> Any:
        try:
            value = self.__getitem__(key)
        except KeyError:
            return return_is_none
        return value

    def del_index(self, index: int) -> None:
        self.table[index][0] = self.DELETED
        self.table[index][1] = None
        self.table[index][2] = None
        self.length -= 1

    def __delitem__(self, key: Any) -> None:
        index = self.get_index(key, self.capacity)
        index = self.find_key(index, key)
        self.del_index(index)
