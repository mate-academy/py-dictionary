from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 2 / 3
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:

        index = self.get_index_for_key(key)

        if self.hash_table[index] is None:
            if int(self.capacity * self.load_factor) <= self.length:
                self.resize()
                index = self.get_index_for_key(key)
            self.length += 1

        self.hash_table[index] = (key, hash(key), value)

    def __getitem__(self, key: Hashable) -> Any:
        index = self.get_index_for_key(key)
        if self.hash_table[index] is None:
            raise KeyError
        return self.hash_table[index][2]

    def get_index_for_key(self, key: Hashable) -> int:
        index = hash(key) % self.capacity
        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.capacity
        return index

    def resize(self) -> None:
        last_table = self.hash_table
        self.length = 0
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        for element in last_table:
            if element is not None:
                key, hash_key, value = element
                index = self.get_index_for_key(key)
                self.length += 1
                self.hash_table[index] = (key, hash_key, value)

    def clear(self) -> None:
        self.hash_table = [None] * self.capacity
        self.length = 0

    def __delitem__(self, key: Hashable) -> None:
        for index in range(len(self.hash_table)):
            if (self.hash_table[index] is not None
                    and self.hash_table[index][0] == key):
                self.hash_table[index] = None
                self.length -= 1
                break

    def get(self, key: Hashable, value: Any = None) -> Any:
        for index in range(len(self.hash_table)):
            if (self.hash_table[index] is not None
                    and self.hash_table[index][0] == key):
                return self.hash_table[index][2]
        return value

    def pop(self, key: Hashable, value: Any = None) -> Any:
        for index in range(len(self.hash_table)):
            if (self.hash_table[index] is not None
                    and self.hash_table[index][0] == key):
                result = self.hash_table[index][2]
                self.hash_table[index] = None
                self.length -= 1
                return result
        if value is not None:
            return value
        raise KeyError

    def update(self, other_dict: "Dictionary") -> None:
        for index in range(len(other_dict.hash_table)):
            if other_dict.hash_table[index] is not None:
                key, hash_key, value = other_dict.hash_table[index]
                self.__setitem__(key, value)
