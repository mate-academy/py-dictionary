from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self.load_factor = self.capacity * (2 / 3)
        self.hash_table = [None] * self.capacity

    def resize_hash_table(self) -> None:
        self.capacity *= 2

        self.load_factor = self.capacity * (2 / 3)

        old_hash_table = self.hash_table
        self.hash_table = [None] * self.capacity

        for item in old_hash_table:
            if item is not None:
                key, value = item
                index = hash(key) % self.capacity

                while self.hash_table[index] is not None:
                    index = (index + 1) % len(self.hash_table)

                self.hash_table[index] = [key, value]

    def find_index(self, key: Hashable) -> int:
        for index, hash_table in enumerate(self.hash_table):
            if hash_table and key == hash_table[0]:
                return index
        return -1

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % self.capacity

        find_index = self.find_index(key)

        if find_index != -1:
            self.hash_table[find_index] = [key, value]

        elif self.hash_table[index] is None:
            self.hash_table[index] = [key, value]
            self.size += 1

        elif isinstance(
                self.hash_table[index], list
        ) and self.hash_table[index][0] == key:

            self.hash_table[index] = [key, value]

        elif (
                self.hash_table[index] is not None
                and self.hash_table[index][0] != key
        ):

            for _ in range(len(self.hash_table)):
                index = (index + 1) % len(self.hash_table)

                if isinstance(self.hash_table[index], list):
                    continue

                self.hash_table[index] = [key, value]
                self.size += 1

                break

        if self.size > self.load_factor:

            self.resize_hash_table()

        print(self.hash_table)
        print(self.size)

    def __getitem__(self, key: Hashable) -> str:
        for item in self.hash_table:
            if item is not None and item[0] == key:
                return item[1]
        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.size
