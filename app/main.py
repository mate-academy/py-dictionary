from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.len_dict = 0
        self.dict_load = 2 / 3
        self.list_dict = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.resize()
        index = hash(key) % self.capacity
        if self.list_dict[index] is None:
            self.len_dict += 1
        else:
            while (self.list_dict[index] is not None
                   and self.list_dict[index][0] != key):
                index = (index + 1) % self.capacity
            if (self.list_dict[index] is not None
                    and self.list_dict[index][0] == key):
                self.list_dict[index][1] = value
            else:
                self.list_dict[index] = (key, value, hash(key))
                self.len_dict += 1
        self.list_dict[index] = [key, value, hash(key)]

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        while self.list_dict[index] is not None:
            if self.list_dict[index][0] == key:
                return self.list_dict[index][1]
            index = (index + 1) % self.capacity
        raise KeyError

    def resize(self) -> None:
        if self.len_dict > self.capacity * self.dict_load:
            self.capacity *= 2
            new_list_dict = self.list_dict[:]
            self.list_dict = [None] * self.capacity
            self.len_dict = 0
            for i in new_list_dict:
                if i is not None:
                    self.__setitem__(i[0], i[1])

    def __len__(self) -> int:
        return self.len_dict
