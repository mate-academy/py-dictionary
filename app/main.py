from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = int(self.capacity * 2 / 3)
        self.resize = 2
        self.length = 0
        self.hash_table = [[] for _ in range(self.capacity)]

    def __len__(self) -> int:
        return self.length

    def get_index_and_hash(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        hash_of_item = hash(key)
        return hash_of_item, index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self.threshold:
            self.resize_table()
        hash_of_item, index = self.get_index_and_hash(key)
        node = [hash_of_item, key, value]
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = node
                self.length += 1
                break
            if (self.hash_table[index][0] == hash_of_item
                    and self.hash_table[index][1] == key):
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def resize_table(self) -> None:
        self.capacity *= self.resize
        self.threshold = int(self.capacity * 2 / 3)
        hash_list = self.hash_table
        self.length = 0
        self.hash_table = [[] for _ in range(self.capacity)]
        for item in hash_list:
            if item:
                self.__setitem__(item[1], item[2])

    def __getitem__(self, key: Hashable) -> Any:
        hash_of_item, index = self.get_index_and_hash(key)
        while self.hash_table[index]:
            if (self.hash_table[index][0] == hash_of_item
                    and self.hash_table[index][1] == key):
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError
