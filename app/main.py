from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.dict_size = 8
        self.dict_length = 0
        self.dict_threshold = int(self.dict_size * 2 / 3)
        self.hash_list = [[]] * self.dict_size

    def resize(self) -> None:
        self.dict_size *= 2
        self.dict_threshold = int(self.dict_size * 2 / 3)
        self.dict_length = 0
        old_data = self.hash_list
        self.hash_list = [[]] * self.dict_size
        for item in old_data:
            if item:
                self.__setitem__(item[0], item[2])

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.dict_length > self.dict_threshold:
            self.resize()
        current_hash = hash(key)
        index = current_hash % self.dict_size
        while True:
            if not self.hash_list[index]:
                self.hash_list[index] = [key, current_hash, value]
                self.dict_length += 1
                break
            if (
                self.hash_list[index][0] == key
                and self.hash_list[index][1] == current_hash
            ):
                self.hash_list[index][2] = value
                break
            index = (index + 1) % self.dict_size

    def __getitem__(self, key: Any) -> list:
        current_hash = hash(key)
        index = current_hash % self.dict_size
        while self.hash_list[index]:
            if (
                self.hash_list[index][1] == current_hash
                and self.hash_list[index][0] == key
            ):
                return self.hash_list[index][2]
            index = (index + 1) % self.dict_size
        raise KeyError

    def __len__(self) -> int:
        return self.dict_length
