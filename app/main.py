from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.size = 8
        self.threshold = int(self.size * 2 / 3)
        self.hash_table = [None for _ in range(self.size)]
        self.length = 0

    def resize_table(self, old_hash_table: list) -> None:
        self.length = 0
        self.size *= 2
        self.threshold = int(self.size * 2 / 3)
        self.hash_table = [None for _ in range(self.size)]
        for data in old_hash_table:
            if data is not None:
                self.__setitem__(data[0], data[1])

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if self.__len__() == self.threshold:
            self.resize_table(self.hash_table)

        if not isinstance(key, Hashable):
            raise TypeError("Key must be Hashable")

        key_hash = hash(key)
        table_index = key_hash % self.size
        while True:
            if self.hash_table[table_index] is None:
                self.hash_table[table_index] = [key, value, key_hash]
                self.length += 1
                break
            if (
                    key_hash == self.hash_table[table_index][2]
                    and key == self.hash_table[table_index][0]
            ):
                self.hash_table[table_index][1] = value
                break
            table_index = (table_index + 1) % self.size

    def __getitem__(self, key: Hashable) -> Any:
        key_hash = hash(key)
        table_index = key_hash % self.size
        while True:
            if self.hash_table[table_index] is None:
                raise KeyError
            if (
                    key_hash == self.hash_table[table_index][2]
                    and key == self.hash_table[table_index][0]
            ):
                return self.hash_table[table_index][1]
            table_index = (table_index + 1) % self.size

    def __len__(self) -> int:
        return self.length
