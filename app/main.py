from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.initial_capacity = 8
        self.load_factor = 2 / 3
        self.hash_table = [None] * self.initial_capacity
        self.number_of_stored_elements = 0

    def find_index(self, key: Hashable) -> int:
        index = hash(key) % self.initial_capacity
        while self.hash_table[index] and self.hash_table[index][0] != key:
            index = (index + 1) % self.initial_capacity
        return index

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self.find_index(key)
        if not self.hash_table[index]:
            if (self.number_of_stored_elements
                    >= int(self.initial_capacity * self.load_factor)):
                self.resize()
                index = self.find_index(key)
            self.number_of_stored_elements += 1
        self.hash_table[index] = (key, hash(key), value)

    def resize(self) -> None:
        self.initial_capacity *= 2
        old_hash_table = self.hash_table
        self.number_of_stored_elements = 0
        self.hash_table = [None] * self.initial_capacity
        for element in old_hash_table:
            if element is not None:
                self[element[0]] = element[2]

    def __getitem__(self, key: Hashable) -> Any:
        index = self.find_index(key)
        if not self.hash_table[index]:
            raise KeyError(f"{key} is not found")
        return self.hash_table[index][2]

    def __len__(self) -> int:
        return self.number_of_stored_elements
