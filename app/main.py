class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self.capacity = initial_capacity
        self.size = 0
        self.table = [None] * self.capacity

    def __setitem__(self, key: object, value: object) -> None:
        if self.size >= self.capacity * 0.75:
            self._resize()

        index = hash(key) % self.capacity
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity
        self.table[index] = (key, value)
        self.size += 1

    def __getitem__(self, key: object) -> object:
        index = hash(key) % self.capacity

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(f"Key {key} not found.")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None:
                self[item[0]] = item[1]
