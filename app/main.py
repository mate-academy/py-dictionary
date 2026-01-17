class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.capacity = 8
        self.hash_table = [None] * self.capacity

    def __len__(self) -> int:
        return self.length

    def __setitem__(self, key: object, value: object) -> None:
        if self.length == 0.75 * self.capacity:
            self.capacity = self.capacity * 2
            new_table = [None] * self.capacity
            for item in self.hash_table:
                if item is not None:
                    index = hash(item[0]) % self.capacity
                    while new_table[index] is not None:
                        index = (index + 1) % self.capacity
                    new_table[index] = item
            self.hash_table = new_table

        index = hash(key) % self.capacity
        while (self.hash_table[index] is not None
               and self.hash_table[index][0] != key):
            index = (index + 1) % self.capacity

        if self.hash_table[index] is None:
            self.length += 1

        self.hash_table[index] = (key, value)

    def __getitem__(self, key: object) -> object:
        index = hash(key) % self.capacity
        while self.hash_table[index] is not None:
            if self.hash_table[index][0] == key:
                return self.hash_table[index][1]
            index = (index + 1) % self.capacity
        raise KeyError(key)
