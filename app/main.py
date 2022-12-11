from __future__ import annotations
from typing import Any, Union


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.size = 8
        self.before_to_resize = int(self.size * 2 / 3)
        self.hash_list = [[] for _ in range(self.size)]

    def __setitem__(self, key: Union[int, float, str, bool, tuple],
                    value: Any) -> None:

        if self.length == self.before_to_resize:
            self.resize()
        hashed_key = hash(key)
        index = hashed_key % self.size
        while True:
            if not self.hash_list[index]:
                self.hash_list[index] = [key, hashed_key, value]
                self.length += 1
                break

            if self.hash_list[index][0] == key and \
                    self.hash_list[index][1] == hashed_key:

                self.hash_list[index][2] = value
                break
            index = (index + 1) % self.size

    def __getitem__(self, key: Union[int, float, str, bool, tuple]) -> Any:
        hashed_key = hash(key)
        index = hashed_key % self.size
        while self.hash_list[index]:
            if self.hash_list[index][0] == key and \
                    self.hash_list[index][1] == hashed_key:

                return self.hash_list[index][2]
            index = (index + 1) % self.size
        raise KeyError

    def resize(self) -> None:
        self.size *= 2
        self.before_to_resize = int(self.size * 2 / 3)
        self.length = 0
        old_hash_list = self.hash_list
        self.hash_list = [[] for _ in range(self.size)]
        for item in old_hash_list:
            if item:
                self.__setitem__(item[0], item[2])

    def __len__(self) -> int:
        return self.length
