from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.len_dictionary = 0
        self.size_dictionary = 8
        self.list_dictionary = [None] * self.size_dictionary

    def __len__(self) -> int:
        return self.len_dictionary

    def find_index(self, key: Hashable) -> int:
        return hash(key) % self.size_dictionary

    def resize_list(self) -> None:
        self.size_dictionary *= 2
        copy_list_dict = self.list_dictionary[:]
        self.list_dictionary = [None] * self.size_dictionary
        self.len_dictionary = 0
        for element in copy_list_dict:
            if element is not None:
                self.__setitem__(element[0], element[1])

    def __getitem__(self, key: Hashable) -> Any:
        index = self.find_index(key)
        while self.list_dictionary[index] is not None:
            if self.list_dictionary[index][0] == key:
                return self.list_dictionary[index][1]
            index = (index + 1) % self.size_dictionary
        raise KeyError(f"Key {key} is not found")

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.len_dictionary > self.size_dictionary * 0.66:
            self.resize_list()
        index = self.find_index(key)

        if self.list_dictionary[index] is None:
            self.len_dictionary += 1
        else:
            while (self.list_dictionary[index] is not None
                   and self.list_dictionary[index][0] != key):
                index = (index + 1) % self.size_dictionary
            if (self.list_dictionary[index] is not None
                    and self.list_dictionary[index][0] == key):
                self.list_dictionary[index][1] = value
            else:
                self.list_dictionary[index] = [key, value, hash(key)]
                self.len_dictionary += 1
        self.list_dictionary[index] = [key, value, hash(key)]
