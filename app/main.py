from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length: int = 0
        self.capacity: int = 8
        self.load_factor: float = 2 / 3
        self.threshold: int = int(self.capacity * self.load_factor) + 1
        self.hash_table: list = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def resize(self) -> None:
        table = [index for index in self.hash_table if index is not None]
        self.capacity *= 2
        self.threshold = int(self.capacity * self.load_factor) + 1
        self.hash_table = [None] * self.capacity
        self.length = 0
        for index in table:
            self.__setitem__(index[0], index[1])

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length == self.threshold:
            self.resize()
        hash_key = hash(key) % self.capacity
        while True:
            if self.hash_table[hash_key] is None:
                self.hash_table[hash_key] = [key, value]
                self.length += 1
                break
            if self.hash_table[hash_key] is not None:
                if self.hash_table[hash_key][0] == key:
                    self.hash_table[hash_key][1] = value
                    break
                hash_key += 1
                if hash_key > len(self.hash_table) - 1:
                    hash_key = 0

    def __getitem__(self, input_key: Any) -> Any:
        hash_ = hash(input_key) % self.capacity
        hash_key = hash_
        while True:
            if self.hash_table[hash_key] is None:
                raise KeyError
            if self.hash_table[hash_key][0] == input_key:
                return self.hash_table[hash_key][1]
            if hash_key == len(self.hash_table) - 1:
                hash_key = 0
                continue
            hash_key += 1

    def clear(self) -> None:
        for index in range(len(self.hash_table)):
            self.hash_table[index] = None

    def get(self, input_key: Any, message: str = "Not found") -> Any:
        for value in self.hash_table:
            if value is not None:
                if value[0] == input_key:
                    return value[1]
        print(message)

    def pop(self, input_key: Any) -> Any:
        for index in range(len(self.hash_table)):
            if self.hash_table[index] is not None:
                if self.hash_table[index][0] == input_key:
                    result = self.hash_table[index][1]
                    self.hash_table[index] = None
                    return result
        raise KeyError

    def update(self, dictionary: dict) -> None:
        for key, value in dictionary.items():
            self.__setitem__(key, value)

    def __delitem__(self, input_key: Any) -> None:
        for index in range(len(self.hash_table)):
            if self.hash_table[index] is not None:
                if self.hash_table[index][0] == input_key:
                    self.hash_table[index] = None
                    return
        raise KeyError
