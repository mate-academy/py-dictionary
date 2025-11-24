from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity

    def insert_new_value(self, table: list, key: Any, value: Any) -> bool:
        index = hash(key) % self.capacity
        if not table[index] or table[index][0] == key:
            exist = bool(not table[index])
            table[index] = [key, value]
            return exist
        else:
            for index, slot in enumerate(table):
                if slot is not None and slot[0] == key:
                    table[index][1] = value
                    return False
            for index, slot in enumerate(table):
                if not slot:
                    table[index] = [key, value]
                    return True
        return False

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= int((self.capacity / 3) * 2):
            self.capacity *= 2
            self.new_hash_table: list = [None] * self.capacity
            for slot in self.hash_table:
                if slot:
                    self.insert_new_value(
                        self.new_hash_table,
                        slot[0],
                        slot[1]
                    )
            self.hash_table = self.new_hash_table
        if self.insert_new_value(self.hash_table, key, value):
            self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index = hash(key) % self.capacity
        if (self.hash_table[index] is not None
                and self.hash_table[index][0] == key):
            return self.hash_table[index][1]
        else:
            for slot in self.hash_table:
                if slot is not None and slot[0] == key:
                    return slot[1]
            raise KeyError

    def __len__(self) -> int:
        return self.length
