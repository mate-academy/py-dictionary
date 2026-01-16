from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.base_length = 8
        self.hash_table: list = [None] * self.base_length
        self.load_factor = 2 / 3

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.length + 1 > self.base_length * self.load_factor:
            self.resize()
        key_hash = hash(key)
        item_index = key_hash % self.base_length
        while self.hash_table[item_index] is not None:
            if key == self.hash_table[item_index][0]:
                self.length -= 1
                break
            item_index += 1
            if item_index >= self.base_length:
                item_index = 0
        self.hash_table[item_index] = (key, key_hash, value)
        self.length += 1

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        item_index = key_hash % self.base_length
        for _ in range(self.base_length):
            if self.hash_table[item_index] is not None:
                if (self.hash_table[item_index][0] == key
                        and self.hash_table[item_index][1] == key_hash):
                    break
            item_index += 1
            if item_index >= self.base_length:
                item_index = 0
        else:
            raise KeyError
        return self.hash_table[item_index][2]

    def resize(self) -> None:
        self.base_length *= 2
        temp_table = [None] * self.base_length
        temp_table, self.hash_table = self.hash_table, temp_table
        self.length = 0
        for item in temp_table:
            if item is not None:
                self.__setitem__(item[0], item[2])
