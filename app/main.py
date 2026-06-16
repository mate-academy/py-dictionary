from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.length = 0
        self.hash_table = [None for _ in range(self.capacity)]

    def get_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def find_slot(self, key: Any, index: int) -> tuple[bool, int]:
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return True, index
            index = (index + 1) % self.capacity
        return False, index

    def resize_table(self) -> None:
        self.capacity *= 2
        old_nodes = [node for node in self.hash_table if node is not None]
        self.hash_table = [None for _ in range(self.capacity)]
        self.length = 0
        for key, _, value in old_nodes:
            self[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        if self.length == int(self.capacity * 2 / 3):
            self.resize_table()

        index = self.get_index(key)
        found, slot_index = self.find_slot(key, index)

        if found:
            self.hash_table[slot_index][2] = value
        else:
            self.hash_table[slot_index] = [key, hash(key), value]
            self.length += 1

    def __getitem__(self, key: Any) -> Any:
        index = self.get_index(key)
        found, slot_index = self.find_slot(key, index)

        if found:
            return self.hash_table[slot_index][2]
        else:
            raise KeyError("Such key doesn't exist.")

    def __len__(self) -> int:
        return self.length
