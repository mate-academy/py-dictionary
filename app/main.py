from typing import Hashable, Any


class Dictionary:
    def __init__(self) -> None:
        self.table_size = 8
        self.count_items = 0
        self.hash_table: list = [None] * self.table_size

    def __len__(self) -> int:
        return self.count_items

    def __getitem__(self, key: Hashable) -> Any:
        index = self._check_index(key)
        if self.hash_table[index] is None:
            raise KeyError(f"Key {key} not found")
        return self.hash_table[index][1]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = self._check_index(key)
        if self.hash_table[index] is None:
            self.count_items += 1
        self.hash_table[index] = [key, value, hash(key)]
        if self.count_items >= self.table_size * 2 / 3:
            self._resize_table()

    def _check_index(self, key: Hashable) -> int:
        hash_key = hash(key)
        index = hash_key % self.table_size
        while (
            self.hash_table[index] is not None
            and self.hash_table[index][0] != key
        ):
            index = (index + 1) % self.table_size
        return index

    def _resize_table(self) -> None:
        self.table_size *= 2
        self.count_items = 0
        temp_hash_table = self.hash_table[:]
        self.hash_table = [None] * self.table_size

        for item in temp_hash_table:
            if item is not None:
                self[item[0]] = item[1]
