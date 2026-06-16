from typing import Any


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.hash_table = [[] for _ in range(self.capacity)]

    def get_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def find_slot(self, key: Any, index: int) -> tuple[bool, int]:
        while self.hash_table[index]:
            if self.hash_table[index][0] == key:
                return True, index
            index = (index + 1) % self.capacity
        return False, index

    def resize_table(self) -> None:
        self.capacity *= 2
        old_nodes = [node for node in self.hash_table if node]
        self.hash_table = [[] for _ in range(self.capacity)]
        for node in old_nodes:
            self[node[0]] = node[2]

    def __setitem__(self, key: Any, value: Any) -> None:
        if len(self) == int(self.capacity * 2 / 3):
            self.resize_table()

        index = self.get_index(key)
        found, slot_index = self.find_slot(key, index)

        if found:
            self.hash_table[slot_index][2] = value
        else:
            self.hash_table[slot_index].extend([key, index, value])

    def __getitem__(self, key: Any) -> Any:
        index = self.get_index(key)
        found, slot_index = self.find_slot(key, index)

        if found:
            return self.hash_table[slot_index][2]
        else:
            raise KeyError("Such key doesn't exist.")

    def __len__(self) -> int:
        return len([node for node in self.hash_table if node])
