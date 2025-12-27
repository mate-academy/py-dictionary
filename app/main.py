from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.dictionary = [None] * 8
        self.capacity = 8

    def __len__(self) -> int:
        length = 0
        for item in self.dictionary:
            if item is not None:
                length += 1
        return length

    def resize(self) -> None:
        old_dictionary = self.dictionary
        self.dictionary = [None] * (self.capacity * 2)
        self.capacity *= 2
        for item in old_dictionary:
            if item is not None:
                self.__setitem__(item[0], item[2])

    def __setitem__(self, key: Any, value: Any) -> None:
        index = hash(key) % len(self.dictionary)
        while self.dictionary[index] is not None:
            if self.dictionary[index][0] == key :
                break
            index = (index + 1) % len(self.dictionary)
        self.dictionary[index] = (key, hash(key), value)
        if len(self) > self.capacity * (2 / 3):
            self.resize()

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % len(self.dictionary)
        count = 0
        if self.dictionary[index] is None:
            raise KeyError
        while self.dictionary[index][0] != key:
            index = (index + 1) % len(self.dictionary)
            count += 1
            if (self.dictionary[index] is None) or (count == self.__len__()):
                raise KeyError

        return self.dictionary[index][2]

    def __str__(self) -> str:
        items = []
        for item in self.dictionary:
            if item is not None:
                items.append(str(item[0]) + ": " + str(item[2]))

        return "{" + ", ".join(items) + "}"
