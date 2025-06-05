from typing import Hashable, Any


class Dictionary:
    def __init__(self, capacity: int = 8, load_factor: float = 2/3) ->None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.table = [None] * capacity
        self.size = 0


    def resize(self, ):
        old_table = self.table
        self.capacity *= 2
        self.clear()
        for data in old_table:
            if data is not None:
                self.__setitem__(data[0], data[1])
        del old_table


    def clear(self) -> None:
        self.table = [None] * self.capacity
        self.size = 0


    def index_element(self, key: Hashable) -> int:
        return hash(key) % self.capacity


    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.index_element(key)
        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.capacity
        if self.table[index] is None:
            self.size += 1
        self.table[index] = (key, value, hash(key))
        if self.size >= self.capacity:
            self.resize()


    def __getitem__(self, key):
        index = self.index_element(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key} not found")


    def __delitem__(self, key: Hashable) -> None:
        index = self.index_element(key)
        if self.table[index] is None:
            raise KeyError
        for _key, _hash, _value in self.table[index]:
            if _key == key and _hash == hash(key):
                self.table[index] = None
                self.size -= 1
                return
        raise KeyError(f"Key {key} not found")

    def __len__(self):
        return self.size
