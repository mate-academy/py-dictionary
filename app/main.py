from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.before_resize = int(self.size * 2 / 3)
        self.hash_table = [[] for _ in range(self.size)]
        self.length = 0

    def __setitem__(
            self,
            key: Hashable,
            value: Any
    ) -> None:
        if self.length == self.before_resize:
            self.resize()
        hashed_key = hash(key)
        index = hashed_key % self.size
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, hashed_key, value]
                self.length += 1
                break

            if self.hash_table[index][0] == key and \
                    self.hash_table[index][1] == hashed_key:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.size

    def __getitem__(
            self,
            key: Hashable
    ) -> Any:
        hashed_key = hash(key)
        index = hashed_key % self.size
        while self.hash_table[index]:
            if self.hash_table[index][0] == key and \
                    self.hash_table[index][1] == hashed_key:
                return self.hash_table[index][2]
            index = (index + 1) % self.size
        raise KeyError

    def resize(self) -> None:
        self.size *= 2
        self.before_resize = int(self.size * 2 / 3)
        self.length = 0
        old_hash_list = self.hash_table
        self.hash_table = [[] for _ in range(self.size)]
        for item in old_hash_list:
            if item:
                self.__setitem__(item[0], item[2])

    def __len__(self) -> int:
        return self.length
