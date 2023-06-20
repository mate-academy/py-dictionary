from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.load_factor = 0.66
        self.hash_table = [None] * self.capacity

    def __add_to_hash_table(self,
                            key: Hashable,
                            key_hash: int,
                            value: Any) -> None:
        _index = key_hash % self.capacity
        while True:
            if not self.hash_table[_index]:
                self.hash_table[_index] = (key, key_hash, value)
                self.length += 1
                break
            elif self.hash_table[_index][0] == key:
                self.hash_table[_index] = (key, key_hash, value)
                break
            _index += 1
            if _index == len(self.hash_table):
                _index = 0

    def __resize_hash_table(self) -> None:
        temp_list = self.hash_table
        self.capacity *= 2
        self.length = 0
        self.hash_table = [None] * self.capacity
        for item in temp_list:
            if item:
                self.__add_to_hash_table(*item)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length == int(self.capacity * self.load_factor):
            self.__resize_hash_table()
        key_hash = hash(key)
        self.__add_to_hash_table(key, key_hash, value)

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        key_index = key_hash % self.capacity
        while self.hash_table[key_index]:
            if self.hash_table[key_index][0] == key:
                return self.hash_table[key_index][2]
            key_index = (key_index + 1) % self.capacity
        raise KeyError(f"No key: {key} in dictionary")

    def __len__(self) -> int:
        return self.length
