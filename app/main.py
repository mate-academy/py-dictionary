import typing


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = int(self.capacity * 2 / 3)
        self.hash_table = [[]] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: typing.Hashable, value: typing.Any) -> None:
        if self.length > self.load_factor:
            self.resize()
        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, hash_key, value]
                self.length += 1
                break
            if self.hash_table[index][0] == key and \
                    self.hash_table[index][1] == hash_key:
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        self.load_factor = int(self.capacity * 2 / 3)
        self.length = 0
        old_table = self.hash_table
        self.hash_table = [[]] * self.capacity
        for item in old_table:
            if item:
                self.__setitem__(item[0], item[2])

    def __getitem__(self, key: str | int) -> list:
        hash_key = hash(key)
        index = hash_key % self.capacity
        while self.hash_table[index]:
            if self.hash_table[index][1] == hash_key and \
                    self.hash_table[index][0] == key:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError

    def clear(self) -> None:
        for storage in self.hash_table:
            storage.clear()
