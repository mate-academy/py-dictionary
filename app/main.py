from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table: list = [None] * self.capacity

    def insert_new_value(self, table: list, key: Any, value: Any) -> bool:
        raw_hash = hash(key)
        start_index = raw_hash % self.capacity
        for probe in range(self.capacity):
            index = (start_index + probe) % self.capacity
            slot = table[index]
            if slot is None:
                table[index] = [key, raw_hash, value]
                return True
            if slot[0] == key:
                table[index][2] = value
                return False

        return False

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length >= int((self.capacity / 3) * 2):
            old_table = self.hash_table
            self.capacity *= 2
            self.new_hash_table: list = [None] * self.capacity
            for slot in old_table:
                if slot:
                    self.insert_new_value(
                        self.new_hash_table,
                        slot[0],
                        slot[2]
                    )
            self.hash_table = self.new_hash_table

        if self.insert_new_value(self.hash_table, key, value):
            self.length += 1

    def __getitem__(self, key: Any) -> Any:
        raw_hash = hash(key)
        start_index = raw_hash % self.capacity

        for probe in range(self.capacity):
            index = (start_index + probe) % self.capacity
            slot = self.hash_table[index]
            if slot is None:
                break
            if slot[0] == key:
                return slot[2]

        raise KeyError(f"Key not found: {key}")

    def __len__(self) -> int:
        return self.length
