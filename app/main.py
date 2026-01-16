from typing import Hashable, Any


class Dictionary:

    def __init__(self, capacity: int = 8, load_factor: float = 0.7) -> None:
        self.capacity = capacity
        self.load_factor = load_factor
        self.threshold = int(self.capacity * self.load_factor)
        self.size = 0
        self.table = [None] * self.capacity

    def table_hash(self, key: Hashable) -> int:
        hash_key = hash(key)
        return hash_key % len(self.table)

    def table_resize(self) -> None:
        old_table = self.table
        self.table = [None] * (len(old_table) * 2)
        self.capacity = len(self.table)
        self.threshold = int(len(self.table) * self.load_factor)
        self.size = 0
        for nod in old_table:
            if nod is not None:
                self.__setitem__(nod[0], nod[2])

    def __setitem__(self, key: Hashable, value: int) -> None:
        number_hash = self.table_hash(key)
        index = number_hash % self.capacity

        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index][2] = value
                return
            index = (index + 1) % self.capacity

        self.table[index] = [key, number_hash, value]
        self.size += 1

        if self.size >= self.threshold:
            self.table_resize()

    def __getitem__(self, key: Hashable) -> Any:
        number_hash = self.table_hash(key)
        index = number_hash % self.capacity
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][2]
            index = (index + 1) % self.capacity

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size
