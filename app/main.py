from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.load_factor = 2 / 3
        self.threshold = int(self.capacity * self.load_factor)
        self.hash_table = [[]] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length > self.threshold:
            self.resize_hash_table()
        key_hash = hash(key)
        index = key_hash % self.capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, key_hash, value]
                self.length += 1
                break
            if (
                self.hash_table[index][0] == key
                and self.hash_table[index][1] == key_hash
            ):
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        index = key_hash % self.capacity

        while self.hash_table[index]:
            stored_key = self.hash_table[index][0]
            stored_key_hash = self.hash_table[index][1]
            stored_value = self.hash_table[index][2]

            if stored_key == key and stored_key_hash == key_hash:
                return stored_value
            index = (index + 1) % self.capacity
        raise KeyError

    def resize_hash_table(self) -> None:
        self.capacity *= 2
        self.threshold = int(self.capacity * self.load_factor)
        self.length = 0
        old_hash_table = self.hash_table
        self.hash_table = [[]] * self.capacity

        for cell in old_hash_table:
            if cell:
                key, value = cell[0], cell[2]
                self.__setitem__(key, value)
