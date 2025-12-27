from typing import Hashable, Any


class Dictionary:

    def __init__(self) -> None:
        self.load_factor = 2 / 3
        self.initial_capacity = 8
        self.hash_table = [[]] * self.initial_capacity
        self.threshold = int(self.initial_capacity * self.load_factor)
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.size >= self.threshold:
            self.resize_hash_table()
        key_hash = hash(key)
        index = key_hash % self.initial_capacity
        while True:
            if not self.hash_table[index]:
                self.hash_table[index] = [key, key_hash, value]
                self.size += 1
                break
            if (
                self.hash_table[index][0] == key
                and self.hash_table[index][1] == key_hash
            ):
                self.hash_table[index][2] = value
                break
            index = (index + 1) % self.initial_capacity

    def __getitem__(self, item: Hashable) -> Any:
        key_hash = hash(item)
        index = key_hash % self.initial_capacity
        while self.hash_table[index]:
            stored_key = self.hash_table[index][0]
            stored_key_hash = self.hash_table[index][1]
            stored_value = self.hash_table[index][2]

            if stored_key == item and stored_key_hash == key_hash:
                return stored_value

            index = (index + 1) % self.initial_capacity
        raise KeyError

    def resize_hash_table(self) -> None:
        self.initial_capacity *= 2
        self.threshold = int(self.initial_capacity * self.load_factor)
        self.size = 0
        old_hash_table = self.hash_table
        self.hash_table = [[]] * self.initial_capacity
        for element in old_hash_table:
            if len(element) == 3:
                key, value = element[0], element[2]
                self.__setitem__(key, value)
