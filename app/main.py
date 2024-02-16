from math import ceil


class Dictionary:
    def __init__(self) -> None:
        self.length_table = 8
        self.load_factor = 0.7
        self.table = [None] * self.length_table
        self.items_in_table = 0

    def __setitem__(self, key: int | str | float,
                    value: int | str | float) -> None:
        index = self.find_available_index(key)
        if not self.table[index]:
            self.resize()
            index = self.find_available_index(key)
            self.items_in_table += 1
        self.table[index] = [key, hash(key), value]

    def resize(self) -> None:
        if self.items_in_table >= ceil(self.length_table * self.load_factor):
            self.items_in_table = 0
            self.length_table *= 2
            old_table = self.table.copy()
            self.table = [None] * self.length_table
            for element in old_table:
                if element:
                    self[element[0]] = element[2]

    def find_available_index(self, key: int | str | float) -> int:
        hash_of_key = hash(key)
        index = hash_of_key % self.length_table
        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.length_table
        return index

    def __getitem__(self, item: int | str | float) -> list:
        index = self.find_available_index(item)
        if not self.table[index]:
            raise KeyError(f"Key {item} not found .")
        return self.table[index][2]

    def __len__(self) -> int:
        return self.items_in_table
