from typing import Any, Hashable


class Dictionary:
    def __init__(self) -> None:
        self.capacity = 8
        self.load_factor = 2 / 3
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def _resize(self) -> None:

        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]

        for sells in self.table:
            for key, value in sells:
                new_index = hash(key) % new_capacity
                new_table[new_index].append((key, value))

        self.capacity = new_capacity
        self.table = new_table

    def __setitem__(self, key: Hashable, value: Hashable) -> Any:
        hash_value = hash(key)
        index = hash_value % self.capacity

        for i, (existing_key, _) in enumerate(self.table[index]):
            if existing_key == key:
                self.table[index][i] = (key, value)
                return

        self.table[index].append((key, value))
        self.size += 1

        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        hash_value = hash(key)
        index = hash_value % self.capacity

        for existing_key, value in self.table[index]:
            if existing_key == key:
                return value

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size
