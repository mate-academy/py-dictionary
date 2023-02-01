from typing import Any, Hashable


class Dictionary:
    def __init__(self, ) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table = [[]] * self.capacity

    def resize(self) -> None:
        first_hash_table = self.hash_table
        self.capacity *= 2
        self.length = 0
        self.hash_table = [[]] * self.capacity
        for hash_key_value in first_hash_table:
            if hash_key_value:
                hash_, key, value = hash_key_value
                self.__setitem__(key, value)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if key is None:
            raise KeyError()
        if self.length > int(self.capacity * 2 / 3):
            self.resize()
        current_hash = hash(key)
        index = current_hash % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = current_hash, key, value
                self.length += 1
                break
            if current_hash == self.hash_table[index][0]\
                    and key == self.hash_table[index][1]:
                self.hash_table[index] = current_hash, key, value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        current_hash = hash(key)
        index = current_hash % self.capacity
        while self.hash_table[index]:
            if current_hash == self.hash_table[index][0]\
                    and key == self.hash_table[index][1]:
                return self.hash_table[index][2]
            index = (index + 1) % self.capacity
        raise KeyError()

    def __len__(self) -> Any:
        return self.length
