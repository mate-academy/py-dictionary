from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.length = 0
        self.critical_size = int(self.size * 2 / 3)
        self.hash_list = [[]] * self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length > self.critical_size:
            self.resize()
        hashes = hash(key)
        index = hashes % self.size
        while True:
            if not self.hash_list[index]:
                self.hash_list[index] = [key, hashes, value]
                self.length += 1
                break
            if self.hash_list[index][0] == key and \
                    self.hash_list[index][1] == hashes:
                self.hash_list[index][2] = value
                break
            index = (index + 1) % self.size

    def resize(self) -> None:
        self.size *= 2
        self.critical_size = int(self.size * 2 / 3)
        self.length = 0
        old_data = self.hash_list
        self.hash_list = [[]] * self.size
        for item in old_data:
            if item:
                self.__setitem__(item[0], item[2])

    def __getitem__(self, key: Any) -> list:
        hashes = hash(key)
        index = hashes % self.size
        while self.hash_list[index]:
            if self.hash_list[index][1] == hashes \
                    and self.hash_list[index][0] == key:
                return self.hash_list[index][2]
            index = (index + 1) % self.size
        raise KeyError

    def __len__(self) -> int:
        return self.length
