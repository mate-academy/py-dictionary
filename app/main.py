from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.load_factor: float = 2 / 3
        self.length: int = 0
        self.hash_table: list = [None] * self.capacity

    def resize(self) -> None:
        self.capacity *= 2
        new_hash_table = [None] * self.capacity
        for items in self.hash_table:
            if items is not None:
                index = hash(items[0]) % len(new_hash_table)
                while new_hash_table[index] is not None:
                    index = (index + 1) % len(new_hash_table)
                else:
                    new_hash_table[index] = items
        self.hash_table = new_hash_table

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % len(self.hash_table)

        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                self.hash_table[index] = [key, hash(key), value]
                break
            index = (index + 1) % len(self.hash_table)
        else:
            self.hash_table[index] = [key, hash(key), value]
            self.length += 1

        if self.length > int(self.capacity * self.load_factor):
            self.resize()

    def __getitem__(self, received_key: Hashable) -> Any:
        index = hash(received_key) % len(self.hash_table)
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == received_key:
                return self.hash_table[index][2]
            else:
                index = (index + 1) % len(self.hash_table)
        else:
            raise KeyError

    def __len__(self) -> int:
        return self.length
