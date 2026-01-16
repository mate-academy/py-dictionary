class Dictionary:
    def __init__(self) -> None:
        self.load_factor = 0.7
        self.capacity = 8
        self.size = 0
        self.hash_table = [None] * self.capacity
        self.DELETED = object()

    def __setitem__(self, key: int, value: int) -> None:
        index = hash(key) % self.capacity
        while (self.hash_table[index] is not None
               and self.hash_table[index] is not self.DELETED):
            k, v = self.hash_table[index]
            if k == key:
                self.hash_table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.hash_table[index] = (key, value)
        self.size += 1

        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __getitem__(self, key: int) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index] is self.DELETED:
                index = (index + 1) % self.capacity
                continue

            k, v = self.hash_table[index]
            if k == key:
                return v
            index = (index + 1) % self.capacity

        raise KeyError(key)

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        old_table = self.hash_table
        self.capacity *= 2
        self.hash_table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item is not None and item is not self.DELETED:
                key, value = item
                self[key] = value

    def __delitem__(self, key: int) -> None:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index] is self.DELETED:
                index = (index + 1) % self.capacity
                continue

            k, v = self.hash_table[index]
            if k == key:
                self.hash_table[index] = self.DELETED
                self.size -= 1
                return
            index = (index + 1) % self.capacity

        raise KeyError(key)
