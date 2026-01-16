from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.table: list = [None] * self.capacity
        for i in range(self.capacity):
            self.table[i] = []
        self.size: int = 0
        self.load_factor: float = 2 / 3
        self.threshold: int = int(self.capacity * self.load_factor)

    def __setitem__(self, key: Hashable, value: Any) -> None:
        index = hash(key) % len(self.table)
        for i, (table_key, table_value) in enumerate(self.table[index]):
            if table_key == key:
                self.table[index][i] = (key, value)
                break
        else:
            self.table[index].append((key, value))
            self.size += 1
            if self.size > self.threshold:
                self.resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % len(self.table)
        for table_key, table_value in self.table[index]:
            if table_key == key:
                return table_value
        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def resize(self) -> None:
        new_table = [[] for _ in range(len(self.table) * 2)]
        for bucket in self.table:
            for key, value in bucket:
                index = hash(key) % len(new_table)
                new_table[index].append((key, value))
        self.table = new_table
        self.threshold = int(len(self.table) * self.load_factor)
