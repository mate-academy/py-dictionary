from typing import Any


class Dictionary:

    LOAD_FACTOR = 2 / 3
    INITIAL_CAPACITY = 8

    def __init__(self) -> None:
        self.capacity = self.INITIAL_CAPACITY
        self._size = 0
        self.table = [None] * self.capacity

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, new_size: int) -> None:
        if new_size >= 0:
            self._size = new_size
        if self.size == round(self.capacity * self.LOAD_FACTOR):
            self.resize()
            self._size = new_size

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        elements = [elem for elem in self.table if elem is not None]
        print(elements)
        self.table = [None] * self.capacity * 2
        self.capacity *= 2

        for element in elements:
            self[element[0]] = element[2]

    def __setitem__(self, key: Any, value: Any) -> None:
        key_index = hash(key) % self.capacity

        if self.table[key_index] is None:
            self.table[key_index] = (key, hash(key), value)
            self.size += 1

        elif self.table[key_index][0] == key:
            if self.table[key_index][1] == hash(key):
                self.table[key_index] = (key, hash(key), value)

        else:
            for i in range(key_index + 1, key_index + self.capacity):
                new_index = i % self.capacity
                if self.table[new_index] is None:
                    self.table[new_index] = (key, hash(key), value)
                    self.size += 1
                    break
                elif (self.table[new_index][0] == key
                      and self.table[new_index][1] == hash(key)):
                    self.table[new_index] = (key, hash(key), value)
                    break

    def __getitem__(self, key: Any) -> Any:
        key_index = hash(key) % self.capacity

        if self.table[key_index] is None:
            raise KeyError("There is no such key in the dictionary!")

        if (self.table[key_index][0] == key
                and self.table[key_index][1] == hash(key)):
            return self.table[key_index][2]

        for i in range(key_index + 1, key_index + self.capacity):
            new_index = i % self.capacity
            if (self.table[new_index][0] == key
                    and self.table[new_index][1] == hash(key)):
                return self.table[new_index][2]
        raise KeyError("There is no such key in dictionary!")

    def clear(self) -> None:
        self.table = [None] * self.capacity
