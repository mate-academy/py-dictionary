from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.threshold = 2 / 3
        self.length = 0
        self.hash_table: list = [None] * self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        cell_index = self.calculate_index(key)

        if self.hash_table[cell_index] is None:
            self.hash_table[cell_index] = (key, hash(key), value)
            self.length += 1

        else:
            while (self.hash_table[cell_index] is not None
                   and self.hash_table[cell_index][0] != key):
                cell_index = (cell_index + 1) % self.capacity

            if (self.hash_table[cell_index] is not None
                    and self.hash_table[cell_index][0] == key):
                self.hash_table[cell_index] = (key, hash(key), value)

            else:
                self.hash_table[cell_index] = (key, hash(key), value)
                self.length += 1

        self.resize_if_necessary()

    def __getitem__(self, key: Hashable) -> None:
        cell_index = self.calculate_index(key)

        while self.hash_table[cell_index] is not None:
            if self.hash_table[cell_index][0] == key:
                return self.hash_table[cell_index][2]
            cell_index = (cell_index + 1) % self.capacity
        raise KeyError

    def __len__(self) -> int:
        return self.length

    def calculate_index(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def clear(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * 8

    def __delitem__(self, key: Hashable) -> None:
        index = self.calculate_index(key)

        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = None
                return
            index = (index + 1) % self.capacity

        raise KeyError

    def resize_if_necessary(self) -> None:
        if self.length / self.capacity > self.threshold:
            old_hash_table = self.hash_table
            self.capacity *= 2
            self.hash_table = [None] * self.capacity
            self.length = 0

            for item in old_hash_table:
                if item is not None:
                    self[item[0]] = item[2]

    def pop(self, key: Hashable, default: None = None) -> Any:
        if key in self.hash_table:
            index = self.calculate_index(key)
            value = self.hash_table[index]
            self.hash_table[index] = None
            return value
        raise KeyError

    def __iter__(self) -> iter:
        for pair in self.hash_table:
            if pair is not None:
                yield pair[0]
