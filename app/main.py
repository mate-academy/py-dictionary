from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [None] * self.capacity
        self.count_current_elements = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        hash_key = hash(key)
        index_table = hash_key % self.capacity
        if self.hash_table[index_table] is None:
            self.hash_table[hash_key % self.capacity] = [key, value, hash_key]
            self.count_current_elements += 1
        else:
            if self.hash_table[index_table][0] == key:
                self.hash_table[index_table] = [key, value, hash_key]

            if self.hash_table[index_table][0] != key:
                while True:
                    if index_table < self.capacity:
                        index_table += 1

                    if index_table == self.capacity:
                        index_table = 0

                    if self.hash_table[index_table] is None:
                        self.hash_table[index_table] = [key, value, hash_key]
                        self.count_current_elements += 1
                        break

                    if self.hash_table[index_table][0] == key:
                        self.hash_table[index_table] = [key, value, hash_key]
                        break

        resize_value = self.capacity * (2 / 3)

        if self.count_current_elements >= resize_value:
            self._resize()

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.count_current_elements = 0

        for el in old_table:
            if el is not None:
                self.__setitem__(el[0], el[1])

    def __getitem__(self, key: Any) -> Any | None:
        hash_key = hash(key)
        index_table = hash_key % self.capacity
        count_iteration = 0
        while True:
            count_iteration += 1
            if self.hash_table[index_table] is None:
                raise KeyError(f"Key not found: {key}")

            if self.hash_table[index_table][0] == key:
                if self.hash_table[index_table][2] == hash_key:
                    return self.hash_table[index_table][1]

            index_table += 1

            if index_table == self.capacity:
                index_table = 0

            if count_iteration >= self.capacity:
                raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.count_current_elements
