from typing import Hashable, Any


class Dictionary:

    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.threshold = int(self.capacity * 2 / 3)
        self.hashtable = [[] for _ in range(self.capacity)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == self.threshold:
            self.resize_hashtable()
        hashed_key = hash(key)
        index = hashed_key % self.capacity
        while True:
            if not self.hashtable[index]:
                self.hashtable[index] = [key, value, hashed_key]
                self.length += 1
                return
            if key == self.hashtable[index][0] and \
                    hashed_key == self.hashtable[index][2]:
                self.hashtable[index][1] = value
                return
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        hash_key = hash(key)
        index = hash_key % self.capacity

        while True:
            if not self.hashtable[index]:
                raise KeyError(key)
            if self.hashtable[index][0] == key and\
                    self.hashtable[index][2] == hash_key:
                return self.hashtable[index][1]
            index = (index + 1) % self.capacity

    def __len__(self) -> int:
        return self.length

    def resize_hashtable(self) -> None:
        copied_hashtable = self.hashtable
        self.length = 0
        self.capacity *= 2
        self.threshold = int(self.capacity * 2 / 3)
        self.hashtable = [[] for _ in range(self.capacity)]
        for item in copied_hashtable:
            if item:
                self.__setitem__(item[0], item[1])
