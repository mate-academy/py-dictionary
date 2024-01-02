from typing import Hashable, Any


class Dictionary:
    INITIAL_CAPACITY = 8
    LOAD_FACTOR = 2 / 3
    RESIZE_VALUE = 2

    def __init__(self) -> None:
        self._size = 0
        self._capacity = self.INITIAL_CAPACITY
        self.hash_table = [[] for _ in range(self._capacity)]

    def __resize_if_loaded(self) -> None:
        if self._size >= self.LOAD_FACTOR * self._capacity:
            self._capacity *= self.RESIZE_VALUE
            self.__refill_table()

    def __refill_table(self) -> None:
        old_data = self.hash_table.copy()
        self.clear()

        for element in old_data:
            if element:
                self.__find_position_and_set_value(*element[1:])

    def __find_position_and_set_value(self, key: Hashable, value: Any) -> None:
        position = self.__find_key_in_table_if_exists(key)
        if position != -1:
            self.hash_table[position][2] = value
            return

        position = hash(key) % self._capacity
        if self.hash_table[position]:
            while self.hash_table[position]:
                position = (position + 1) % self._capacity

        self.hash_table[position] = [hash(key), key, value]
        self._size += 1

    def __find_key_in_table_if_exists(self, key: Hashable) -> int:
        for index in range(len(self.hash_table)):
            if self.hash_table[index]:
                if self.hash_table[index][1] == key:
                    return index

        return -1

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.__resize_if_loaded()
        self.__find_position_and_set_value(key, value)

    def __getitem__(self, key: Hashable) -> Any:
        position = self.__find_key_in_table_if_exists(key)
        if position == -1:
            raise KeyError(f"{key} not in dictionary")

        return self.hash_table[position][2]

    def __len__(self) -> int:
        return self._size

    def __delitem__(self, key: Hashable) -> None:
        del self.hash_table[self.__find_key_in_table_if_exists(key)]
        self.__refill_table()

    def pop(self, key: Hashable) -> Any:
        element = self[key]
        del self[key]
        return element

    def clear(self) -> None:
        self.hash_table = [[] for _ in range(self._capacity)]
        self._size = 0

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default
