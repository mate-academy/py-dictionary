from typing import Hashable, Any


class Dictionary:
    pass

    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.length = 0
        self.hash_table = [None for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            if self.hash_table[index] is None:
                self.hash_table[index] = [key, value, key_hash]
                self.length += 1
                break
            if self.hash_table[index][2] == key_hash and \
                    self.hash_table[index][0] == key:
                self.hash_table[index] = [key, value, key_hash]
                break
            index = (index + 1) % self.capacity
        if self.length == self.threshold:
            self.resize()

    def resize(self) -> None:
        temp_table = self.hash_table
        self.capacity *= 2
        self.length = 0
        self.threshold = int(self.capacity * 2 / 3)
        self.hash_table = [None for _ in range(self.capacity)]
        for item in temp_table:
            if item is not None:
                self.__setitem__(item[0], item[1])

    def __getitem__(self, input_key: Hashable) -> Any:
        key_hash = hash(input_key)
        index = key_hash % self.capacity
        while True:
            if not self.hash_table[index]:
                raise KeyError("Key Error")
            if self.hash_table[index][2] == key_hash and\
                    self.hash_table[index][0] == input_key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.hash_table.clear()

    def __delitem__(self, key: Hashable) -> None:
        key_hash = hash(key)
        index = key_hash % self.capacity
        self.hash_table[index] = None
        temp_table = self.hash_table
        self.length = 0
        self.hash_table = [None for _ in range(self.capacity)]
        for item in temp_table:
            if item is not None:
                self.__setitem__(item[0], item[1])

    def get(self, key: Hashable) -> Any:
        return self.__getitem__(key)

    def pop(self, key: Hashable) -> Any:
        element = self.__getitem__(key)
        self.__delitem__(key)
        return element
