from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        hash_item = hash(key)
        if int(self.capacity * 2 / 3) == self.length:
            temp = [element for element in self.hash_table if element]
            self.capacity *= 2
            self.hash_table = [None] * self.capacity
            for element in temp:
                index = element[1] % self.capacity
                if self.hash_table[index]:
                    while self.hash_table[index]:
                        index = (index + 1) % self.capacity
                self.hash_table[index] = element

        index = hash_item % self.capacity
        if self.hash_table[index]:
            while self.hash_table[index]:
                if (
                    self.hash_table[index][0] == key
                    and self.hash_table[index][1] == hash_item
                ):
                    self.hash_table[index][2] = value
                    return
                index = (index + 1) % self.capacity
        self.hash_table[index] = [key, hash_item, value]
        self.length += 1

    def __getitem__(self, item: Hashable) -> Any:
        hash_item = hash(item)
        index = hash_item % self.capacity
        if self.hash_table[index]:
            start_index = index
            while True:
                if (
                    self.hash_table[index][0] == item
                    and self.hash_table[index][1] == hash_item
                ):
                    return self.hash_table[index][2]
                index = (index + 1) % self.capacity
                if index == start_index:
                    break
        raise KeyError("Key not found")

    def __len__(self) -> int:
        return self.length
