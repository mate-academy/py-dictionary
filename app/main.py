from typing import Any, Hashable


class Dictionary:
    LOAD_FACTOR = 2 / 3

    def __init__(self) -> None:
        self.buckets = [[] for _ in range(8)]
        self.size = 0
        self.capacity = len(self.buckets)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.count_index(key)

        while self.buckets[index]:
            key_, _, _ = self.buckets[index]
            if key == key_:
                self.buckets[index] = (key, hash(key), value)
                return
            index = (index + 1) % self.capacity

        self.size += 1
        self.buckets[index] = (key, hash(key), value)
        self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = self.count_index(key)

        while self.buckets[index]:
            key_, _, value = self.buckets[index]
            if key == key_:
                return value
            index = (index + 1) % self.capacity

        raise KeyError

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        threshold = self.capacity * self.LOAD_FACTOR

        if self.size <= threshold:
            return

        self.capacity *= 2
        old_dictionary = self.buckets

        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

        for element in old_dictionary:
            if element:
                key, _, value = element
                self.__setitem__(key, value)

    def count_index(self, new_key: Hashable) -> int:
        hashed_value = hash(new_key)
        index = hashed_value % self.capacity

        return index
