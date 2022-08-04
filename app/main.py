import math


class Dictionary:
    THRESHOLD = 8
    LOAD_FACTOR = 2 / 3
    RESIZE_COEFFICIENT = 2

    def __init__(self):
        self.capacity = Dictionary.THRESHOLD
        self.length = 0
        self.hash_table: list[tuple | None] = [None] * 8

    def __setitem__(self, key, value):
        hash_index = hash(key) % self.capacity

        while self.hash_table[hash_index] is not None:
            if self.hash_table[hash_index][0] == key:
                self.hash_table[hash_index] = (key, value)
                return

            hash_index = (hash_index + 1) % self.capacity

        self.length += 1
        if self.length > math.floor(self.capacity * Dictionary.LOAD_FACTOR):
            self.__resize_dict()
            self.__setitem__(key=key, value=value)
            return

        self.hash_table[hash_index] = (key, value)

    def __resize_dict(self):
        self.length = 0
        self.capacity *= Dictionary.RESIZE_COEFFICIENT
        elements = [el for el in self.hash_table if el is not None]
        self.hash_table = [None] * self.capacity

        for el in elements:
            self.__setitem__(key=el[0], value=el[1])

    def __getitem__(self, key):
        hash_index = hash(key) % self.capacity

        while self.hash_table[hash_index] is not None:
            if self.hash_table[hash_index][0] == key:
                return self.hash_table[hash_index][1]

            hash_index = (hash_index + 1) % self.capacity

        raise KeyError("No keys!")

    def __len__(self):
        return self.length

    def __repr__(self):
        result = {el for el in self.hash_table if el is not None}
        return f"{result}"
