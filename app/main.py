from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.dict_len = 0
        self.capacity = 8
        self.hash_table = [()] * self.capacity
        self.capacity_limit = self.capacity * 2 // 3

    def __setitem__(self, key: Any, value: Any) -> None :
        if self.dict_len >= self.capacity_limit:
            self.capacity *= 2
            self.capacity_limit = self.capacity * 2 // 3
            self.hash_table = self.increase_hash_table()

        addiction_index = 0
        while addiction_index < len(self.hash_table):
            index = hash(key) % self.capacity + addiction_index
            if self.hash_table[index] == ():
                self.hash_table[index] = (hash(key), key, value)
                self.dict_len += 1
                break
            elif self.hash_table[index][1] == key:
                self.hash_table[index] = (hash(key), key, value)
                break
            addiction_index += 1

    def __getitem__(self, key: Any) -> None:
        addiction_index = 0
        while addiction_index < len(self.hash_table):
            index = hash(key) % self.capacity + addiction_index
            try:
                if self.hash_table[index][1] == key:
                    return self.hash_table[index][2]
            except IndexError:
                raise KeyError
            addiction_index += 1

    def __len__(self) -> int:
        return self.dict_len

    def increase_hash_table(self) -> list:
        increased_table = [()] * self.capacity
        for value in self.hash_table:
            if not value:
                continue

            addiction_index = 0
            while addiction_index < len(increased_table):
                index = value[0] % self.capacity + addiction_index
                if (
                    increased_table[index] == ()
                    or increased_table[index][1] == value[1]
                ):
                    increased_table[index] = value
                    break
                addiction_index += 1

        return increased_table
