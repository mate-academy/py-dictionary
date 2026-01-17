from typing import Any, Hashable


class Dictionary:
    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.table = [None] * self.capacity
        self.load_factor = round(0.66 * self.capacity)
        self.length = 0

    def resize_dictionary(self, table_to_resize: list) -> None:
        old_table = table_to_resize.copy()
        self.capacity *= 2
        self.length = 0
        self.table = [None] * self.capacity
        self.load_factor = round(0.66 * self.capacity)
        for cell in old_table:
            if cell is not None:
                self.__setitem__(cell[0], cell[1])

    def __setitem__(self, key: Any, value: Any) -> None:
        if not isinstance(key, Hashable):
            raise TypeError("Key must be hashable!")

        if self.length + 1 >= self.load_factor:
            self.resize_dictionary(self.table)

        hash_key = hash(key)
        index = hash_key % self.capacity
        while True:
            if self.table[index] is None:
                self.table[index] = [key, value, hash_key]
                self.length += 1
                break
            if (self.table[index][0] == key
                    and self.table[index][2] == hash_key):
                self.table[index][1] = value
                break
            index = (index + 1) % self.capacity

    def __getitem__(self, item: any) -> None:
        hash_key = hash(item)
        index = hash_key % self.capacity
        first_index = index
        while self.table[index] is not None:
            if (self.table[index][0] == item
                    and self.table[index][2] == hash_key):
                return self.table[index][1]
            index = (index + 1) % self.capacity
            if index == first_index:
                break

        raise KeyError("Key does not exist!")

    def __len__(self) -> int:
        return self.length
