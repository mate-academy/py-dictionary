class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * self.capacity

    def _hash(self, key: int | str) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_table = [None] * new_capacity

        for node in self.table:
            if node:
                new_index = hash(node[0]) % new_capacity
                while new_table[new_index] is not None:
                    new_index = (new_index + 1) % new_capacity
                new_table[new_index] = node

        self.capacity = new_capacity
        self.table = new_table

    def __setitem__(self, key: int | str, value: int | str) -> None:
        if self.size >= self.capacity * 0.7:
            self._resize()

        index = self._hash(key)

        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, value)
        self.size += 1

    def __getitem__(self, key: int | str) -> None:
        index = self._hash(key)

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity

        raise KeyError(f"Key '{key}' not found")

    def __len__(self) -> int:
        return self.size
