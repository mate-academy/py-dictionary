from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = round(2 / 3, 2)
        self.dictionary = [None] * self.capacity
        self.size = 0

    def __setitem__(self, key: int | str, value: Any) -> None:
        if self.size >= self.capacity * self.load_factor:
            self.resize_dictionary()

        index = self.find_index_in_dict(key)

        if self.dictionary[index] is None:
            self.size += 1

        self.dictionary[index] = (hash(key), key, value)

    def resize_dictionary(self) -> None:
        old_dict = self.dictionary
        self.capacity *= 2
        self.size = 0
        self.dictionary = [None] * self.capacity

        for items in old_dict:
            if items is not None:
                self.__setitem__(items[1], items[2])

    def find_index_in_dict(self, key: int | str) -> int:
        hash_code = hash(key)

        index = hash_code % self.capacity

        while (self.dictionary[index] is not None
               and (self.dictionary[index][0] != hash_code
                    or self.dictionary[index][1] != key)):
            index += 1
            index %= self.capacity

        return index

    def __getitem__(self, key: int | str) -> Any:
        index = self.find_index_in_dict(key)

        if self.dictionary[index] is None:
            raise KeyError

        return self.dictionary[index][2]

    def __len__(self) -> int:
        return self.size
