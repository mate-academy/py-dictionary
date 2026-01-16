from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.length = 0
        self.threshold = int(self.size * 2 / 3)
        self.hash_list = [[]] * self.size

    def resize(self) -> None:
        self.size *= 2
        self.threshold = int(self.size * 2 / 3)
        self.length = 0
        old_data = self.hash_list
        self.hash_list = [[]] * self.size
        for value in old_data:
            if value:
                self.__setitem__(value[0], value[2])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self.threshold:
            self.resize()

        current_hash = hash(key)
        index = current_hash % self.size

        while True:
            if not self.hash_list[index]:
                self.hash_list[index] = [key, current_hash, value]
                self.length += 1
                break
            if (
                self.hash_list[index][0] == key
                and self.hash_list[index][1] == current_hash
            ):
                self.hash_list[index][2] = value
                break
            index = (index + 1) % self.size

    def __getitem__(self, key: Hashable) -> list:
        current_hash = hash(key)
        index = current_hash % self.size
        while self.hash_list[index]:
            if (
                self.hash_list[index][0] == key
                and self.hash_list[index][1] == current_hash
            ):
                return self.hash_list[index][2]
            index = (index + 1) % self.size
        raise KeyError

    def __len__(self) -> int:
        return self.length
