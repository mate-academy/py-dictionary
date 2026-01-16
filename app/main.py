from typing import Callable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.resize = 2
        self.length = 0
        self.hash_table = [None] * self.capacity

    def __setitem__(self, key: Callable, value: Callable) -> None:
        index = hash(key) % self.capacity
        while (self.hash_table[index] is not None
               or self.hash_table[index] == 1):
            if self.hash_table[index][0] == key or self.hash_table[index] == 1:
                self.length -= 1
                break
            index = (index + 1) % self.capacity
        self.hash_table[index] = (key, value)
        self.length += 1
        if len(self) > self.load_factor * self.capacity:
            self.make_resize()

    def make_resize(self) -> None:
        self.capacity *= self.resize
        old_hash_table = self.hash_table
        self.hash_table = [None] * self.capacity
        self.length = 0
        for item in old_hash_table:
            if item is not None:
                key, value = item
                self.__setitem__(key, value)

    def __getitem__(self, key: Callable) -> Callable:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            current_key, value = self.hash_table[index]
            if current_key == key:
                return value
            index = (index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def clear(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.resize = 2
        self.length = 0
        self.hash_table = [None] * self.capacity

    def __delitem__(self, key: Callable) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index] != 1:
                current_key, value = self.hash_table[index]
                if current_key == key:
                    self.hash_table[index] = 1
            index = (index + 1) % self.capacity
        self.length -= 1

    def get(self, key: Callable, value: Callable = None) -> Callable:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            current_key, current_value = self.hash_table[index]
            if current_key == key:
                return current_value
            index = (index + 1) % self.capacity
        return value

    def pop(self, key: Callable, default: Callable = None) -> Callable:
        value = self.get(key)
        del self[key]
        if value is None and default is None:
            raise KeyError
        if value is None:
            return default
        return value

    def update(self, other: Callable) -> None:
        for element in other:
            self[element[0]] = element[1]

    def __iter__(self) -> Callable:
        self.iter_index = 0
        self.number_of_iter = 0
        return self

    def __next__(self) -> Callable:
        if self.number_of_iter == len(self):
            raise StopIteration
        for index in range(self.iter_index, self.capacity):
            if (self.hash_table[index] is not None
                    and self.hash_table[index] != 1):
                self.iter_index = index + 1
                self.number_of_iter += 1
                return self.hash_table[index]
